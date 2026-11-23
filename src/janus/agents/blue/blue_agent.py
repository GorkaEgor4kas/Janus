from uuid import uuid4

from janus.agents.agent import Agent
from janus.domain.action import Action
from janus.domain.agent_state import AgentStatus
from janus.domain.decision import DecisionType, SecurityDecision
from janus.event_bus.event_bus import EventBus
from janus.event_bus.events import Event, EventType
from janus.gateway.security_gateway import SecurityGateway


class BlueTeamAgent(Agent):
    def __init__(
        self,
        agent_id: str,
        session_id: str,
        target_id: str,
        event_bus: EventBus,
        security_gateway: SecurityGateway,
    ) -> None:
        super().__init__(agent_id=agent_id)
        if event_bus is not security_gateway.event_bus:
            raise ValueError("BlueTeamAgent and SecurityGateway must share the same EventBus.")

        self.session_id = session_id
        self.target_id = target_id
        self.event_bus = event_bus
        self.security_gateway = security_gateway

    def start(self) -> None:
        if self.state.status == AgentStatus.RUNNING:
            raise RuntimeError(f"Agent {self.state.agent_id} is already running.")

        self.state.status = AgentStatus.RUNNING
        self.event_bus.subscribe(
            EventType.ACTION_REQUESTED,
            self._on_action_requested,
        )
        self._publish_event(
            EventType.COMPONENT_READY,
            {"component_id": self.state.agent_id, "component_type": "blue_team_agent"},
        )

    def stop(self) -> None:
        self.state.status = AgentStatus.STOPPED

    def _on_action_requested(self, event: Event) -> None:
        if self.state.status != AgentStatus.RUNNING:
            return
        if event.session_id != self.session_id:
            return

        action_data = event.payload.get("action")
        if not isinstance(action_data, dict):
            raise ValueError("Action request event must contain an 'action' object.")

        action = Action.model_validate(action_data)
        if action.session_id != event.session_id:
            raise ValueError("Action session_id does not match its event session_id.")

        decision = self._evaluate_action(action)
        self.event_bus.publish(
            Event(
                event_id=str(uuid4()),
                session_id=action.session_id,
                event_type=EventType.SECURITY_DECISION_MADE,
                source=self.state.agent_id,
                payload={"decision": decision.model_dump(mode="json")},
            )
        )

    def _evaluate_action(self, action: Action) -> SecurityDecision:
        """Return a fail-closed decision until Blue Team policy is implemented."""
        if action.target_id != self.target_id:
            reason = "Action target is outside this Blue Team agent's configured scope."
        else:
            reason = "Blue Team policy is not implemented; action is denied by default."

        return SecurityDecision(
            decision_id=str(uuid4()),
            action_id=action.action_id,
            session_id=action.session_id,
            decision=DecisionType.BLOCKED,
            reason=reason,
        )

    def _publish_event(self, event_type: EventType, payload: dict[str, str]) -> None:
        self.event_bus.publish(
            Event(
                event_id=str(uuid4()),
                session_id=self.session_id,
                event_type=event_type,
                source=self.state.agent_id,
                payload=payload,
            )
        )
