from janus.domain.action import Action, ActionType
from janus.domain.action_result import ActionResult, ResultStatus

from janus.event_bus.event_bus import EventBus

from janus.domain.decision import DecisionType, SecurityDecision
from janus.event_bus.events import Event, EventType


class SecurityGateway:
    def __init__(self, target, event_bus: EventBus):
        self.target = target
        self.event_bus = event_bus
        self._pending_sessions: dict[str, str] = {}
        self._decisions: dict[str, SecurityDecision] = {}
        self.event_bus.subscribe(
            EventType.SECURITY_DECISION_MADE,
            self._on_security_decision,
        )

    def handle_action(self, action: Action) -> ActionResult:
        """Publish an action, await a synchronous bus decision, then execute only if allowed."""
        if action.action_id in self._pending_sessions:
            raise ValueError(f"Action is already being handled: {action.action_id}")

        self._pending_sessions[action.action_id] = action.session_id
        try:
            self.event_bus.publish(
                Event(
                    event_id=f"{action.action_id}:requested",
                    session_id=action.session_id,
                    event_type=EventType.ACTION_REQUESTED,
                    source=action.actor_id,
                    payload={"action": action.model_dump(mode="json")},
                )
            )
            decision = self._decisions.pop(action.action_id, None)
        finally:
            self._pending_sessions.pop(action.action_id, None)
            self._decisions.pop(action.action_id, None)

        if decision is None:
            return self._make_result(
                action,
                ResultStatus.BLOCKED,
                error="No security decision received; action was not executed.",
            )

        if decision.decision != DecisionType.ALLOWED:
            self.event_bus.publish(
                Event(
                    event_id=f"{action.action_id}:blocked",
                    session_id=action.session_id,
                    event_type=EventType.ACTION_BLOCKED,
                    source="security_gateway",
                    payload={
                        "action_id": action.action_id,
                        "decision_id": decision.decision_id,
                        "reason": decision.reason,
                    },
                )
            )
            return self._make_result(
                action,
                ResultStatus.BLOCKED,
                error=decision.reason,
            )

        validation_error = self._validate_action(action)
        if validation_error is not None:
            self.event_bus.publish(
                Event(
                    event_id=f"{action.action_id}:invalid",
                    session_id=action.session_id,
                    event_type=EventType.ACTION_BLOCKED,
                    source="security_gateway",
                    payload={
                        "action_id": action.action_id,
                        "decision_id": decision.decision_id,
                        "reason": validation_error,
                    },
                )
            )
            return self._make_result(
                action,
                ResultStatus.BLOCKED,
                error=validation_error,
            )

        self.event_bus.publish(
            Event(
                event_id=f"{action.action_id}:allowed",
                session_id=action.session_id,
                event_type=EventType.ACTION_ALLOWED,
                source="security_gateway",
                payload={
                    "action_id": action.action_id,
                    "decision_id": decision.decision_id,
                },
            )
        )

        try:
            response = self._execute_action(action)
            self.event_bus.publish(
                Event(
                    event_id=f"{action.action_id}:executed",
                    session_id=action.session_id,
                    event_type=EventType.ACTION_EXECUTED,
                    source="security_gateway",
                    payload={"action_id": action.action_id},
                )
            )
            return self._make_result(
                action,
                ResultStatus.SUCCESS,
                output={"response": response},
            )

        except Exception as e:
            self.event_bus.publish(
                Event(
                    event_id=f"{action.action_id}:execution_failed",
                    session_id=action.session_id,
                    event_type=EventType.ACTION_EXECUTION_FAILED,
                    source="security_gateway",
                    payload={
                        "action_id": action.action_id,
                        "error": str(e),
                    },
                )
            )
            return self._make_result(
                action,
                ResultStatus.FAILED,
                error=str(e),
            )

    ### Need to understand this topic better
    def _on_security_decision(self, event: Event) -> None:
        decision_data = event.payload.get("decision")
        if not isinstance(decision_data, dict):
            raise ValueError("Security decision event must contain a 'decision' object.")

        action_id = decision_data.get("action_id")
        session_id = self._pending_sessions.get(action_id)
        if session_id is None:
            return

        decision = SecurityDecision.model_validate(decision_data)
        if decision.session_id != session_id or event.session_id != session_id:
            raise ValueError("Security decision does not match the pending action's session.")
        if action_id in self._decisions:
            raise ValueError(f"Multiple security decisions received for action {action_id}.")

        self._decisions[action_id] = decision

    def _validate_action(self, action: Action) -> str | None:
        if action.action_type not in (ActionType.MESSAGE, ActionType.PROMPT, ActionType.TOOL_CALL):
            return f"Unsupported action type: {action.action_type.value}"

        prompt = action.payload.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            return "Action payload must contain a non-empty 'prompt' string."

        unexpected_fields = action.payload.keys() - {"prompt", "max_steps"}
        if unexpected_fields:
            return f"Unexpected action payload fields: {', '.join(sorted(unexpected_fields))}"

        max_steps = action.payload.get("max_steps", 5)
        if isinstance(max_steps, bool) or not isinstance(max_steps, int) or max_steps <= 0:
            return "'max_steps' must be a positive integer."

        return None

    def _execute_action(self, action: Action) -> str:
        return self.target.handle(
            prompt=action.payload["prompt"],
            max_steps=action.payload.get("max_steps", 5),
        )

    def _make_result(
        self,
        action: Action,
        status: ResultStatus,
        *,
        output: dict | None = None,
        error: str | None = None,
    ) -> ActionResult:
        result = ActionResult(
            result_id=f"{action.action_id}:result",
            action_id=action.action_id,
            session_id=action.session_id,
            status=status,
            output=output or {},
            error=error,
        )
        self.event_bus.publish(
            Event(
                event_id=f"{action.action_id}:result-event",
                session_id=action.session_id,
                event_type=EventType.ACTION_RESULT_RECEIVED,
                source="security_gateway",
                payload={"result": result.model_dump(mode="json")},
            )
        )
        return result
