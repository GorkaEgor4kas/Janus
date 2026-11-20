import json
import uuid
from dataclasses import dataclass

from janus.agents.agent import Agent

from janus.domain.action import Action, ActionType
from janus.domain.action_result import ActionResult
from janus.domain.agent_state import AgentStatus

from janus.gateway.security_gateway import SecurityGateway

from janus.llm.client import LLMClient
from janus.system_prompts_test.planner_system_prompt_test import PLANNER_SYSTEM_PROMPT
from janus.system_prompts_test.evaluator_system_prompt_test import EVALUATOR_SYSTEM_PROMPT


@dataclass(frozen=True)
class EvaluationResult:
    goal_achieved: bool
    rationale: str
    needs_clarification: bool = False


class RedTeamAgent(Agent):
    def __init__(
            self,
            goal: str,
            agent_id: str,
            session_id: str,
            llm_client: LLMClient,
            max_steps: int,
            security_gateway: SecurityGateway,
            target_id: str,
            ):
        if not goal.strip():
            raise ValueError("goal must not be empty.")
        if (
            isinstance(max_steps, bool)
            or not isinstance(max_steps, int)
            or max_steps <= 0
        ):
            raise ValueError("max_steps must be greater than zero.")

        super().__init__(agent_id=agent_id)
        self.goal = goal
        self.session_id = session_id
        self.llm_client = llm_client
        self.max_steps = max_steps
        self.security_gateway = security_gateway
        self.target_id = target_id

        self.action_history: list[dict[str, object]] = []
        self.current_step = 0

    def start(self) -> None:
        if self.state.status == AgentStatus.RUNNING:
            raise RuntimeError(f"Agent {self.state.agent_id} is already running.")

        self.state.status = AgentStatus.RUNNING
        self.current_step = 0
        self.action_history.clear()

        try:
            self._run_loop()
        except Exception:
            self.state.status = AgentStatus.ERROR
            raise

    def stop(self) -> None:
        self.state.status = AgentStatus.STOPPED

    def _run_loop(self) -> None:
        """Plan, submit, and evaluate up to the configured action limit."""
        for _ in range(self.max_steps):
            if self.state.status != AgentStatus.RUNNING:
                return

            action = self._planner(self.goal, action_history=self.action_history)
            action_result = self.security_gateway.handle_action(action)
            evaluation = self._evaluator(
                action_result=action_result,
                goal=self.goal,
                action=action,
                action_history=self.action_history,
            )
            self.action_history.append(
                {
                    "action": action.model_dump(mode="json"),
                    "result": action_result.model_dump(mode="json"),
                    "evaluation": {
                        "goal_achieved": evaluation.goal_achieved,
                        "rationale": evaluation.rationale,
                        "needs_clarification": evaluation.needs_clarification,
                    },
                }
            )
            self.current_step += 1

            if evaluation.goal_achieved or evaluation.needs_clarification:
                self.state.status = AgentStatus.STOPPED
                return

        self.state.status = AgentStatus.STOPPED

    def _planner(
        self,
        goal: str,
        action_history: list[dict[str, object]],
    ) -> Action:
        """Generate and validate one proposed prompt action."""
        response = self.llm_client.chat([
            {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Goal: {goal}\n"
                    f"Action history: {json.dumps(action_history, ensure_ascii=False)}"
                ),
            },
        ])
        planner_output = self._parse_json_object(response, "planner")

        if planner_output.get("status") == "needs_clarification":
            if set(planner_output) != {"status", "question"}:
                raise ValueError("Planner clarification response contains unexpected fields.")
            question = planner_output.get("question")
            if not isinstance(question, str) or not question.strip():
                raise ValueError("Planner returned an invalid clarification response.")
            raise ValueError(f"Planner needs clarification: {question}")

        if planner_output.get("status") != "proposed":
            raise ValueError("Planner response must have status 'proposed'.")
        if set(planner_output) != {"status", "action_type", "payload", "rationale"}:
            raise ValueError("Planner response contains missing or unexpected fields.")
        if planner_output["action_type"] != ActionType.PROMPT.value:
            raise ValueError("Planner may only propose prompt actions.")

        payload = planner_output["payload"]
        if not isinstance(payload, dict) or set(payload) != {"prompt"}:
            raise ValueError("Planner payload must contain only a 'prompt' field.")
        prompt = payload["prompt"]
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Planner payload 'prompt' must be a non-empty string.")
        rationale = planner_output["rationale"]
        if not isinstance(rationale, str) or not rationale.strip():
            raise ValueError("Planner rationale must be a non-empty string.")

        return Action(
            action_id=str(uuid.uuid4()),
            session_id=self.session_id,
            actor_id=self.state.agent_id,
            target_id=self.target_id,
            action_type=ActionType.PROMPT,
            payload=payload,
        )

    def _evaluator(
        self,
        action_result: ActionResult,
        goal: str,
        action: Action,
        action_history: list[dict[str, object]],
    ) -> EvaluationResult:
        """Evaluate goal achievement from the observed action and result."""
        response = self.llm_client.chat([
            {"role": "system", "content": EVALUATOR_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Goal: {goal}\n"
                    f"Action: {json.dumps(action.model_dump(mode='json'), ensure_ascii=False)}\n"
                    f"Result: {json.dumps(action_result.model_dump(mode='json'), ensure_ascii=False)}\n"
                    f"Relevant history: {json.dumps(action_history, ensure_ascii=False)}"
                ),
            },
        ])
        output = self._parse_json_object(response, "evaluator")

        if output.get("status") == "needs_clarification":
            if set(output) != {"status", "question"}:
                raise ValueError("Evaluator clarification response contains unexpected fields.")
            question = output.get("question")
            if not isinstance(question, str) or not question.strip():
                raise ValueError("Evaluator returned an invalid clarification response.")
            return EvaluationResult(
                goal_achieved=False,
                rationale=question,
                needs_clarification=True,
            )

        if set(output) != {"goal_achieved", "rationale"}:
            raise ValueError("Evaluator response contains missing or unexpected fields.")
        goal_achieved = output["goal_achieved"]
        rationale = output["rationale"]
        if not isinstance(goal_achieved, bool):
            raise ValueError("Evaluator field 'goal_achieved' must be a boolean.")
        if not isinstance(rationale, str) or not rationale.strip():
            raise ValueError("Evaluator field 'rationale' must be a non-empty string.")

        return EvaluationResult(goal_achieved=goal_achieved, rationale=rationale)

    @staticmethod
    def _parse_json_object(response: str, component: str) -> dict[str, object]:
        try:
            parsed = json.loads(response)
        except json.JSONDecodeError as error:
            raise ValueError(f"{component.capitalize()} returned invalid JSON.") from error
        if not isinstance(parsed, dict):
            raise ValueError(f"{component.capitalize()} response must be a JSON object.")
        return parsed