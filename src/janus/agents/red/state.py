from pydantic import Field
from janus.domain.agent_state import AgentState, AgentStatus

class RedState(AgentState):
    session_id: str
    agent_id: str

    status: AgentStatus = AgentStatus.IDLE

    max_steps: int = Field(gt=0)
    current_step: int = Field(default=0, ge=0)

    current_goal: str | None = None
    current_phase: str | None = None

