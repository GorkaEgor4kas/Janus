from enum import StrEnum
from pydantic import BaseModel, Field

class AgentStatus(StrEnum):
    IDLE = "idle"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"


class AgentState(BaseModel):
    agent_id: str
    status: AgentStatus

