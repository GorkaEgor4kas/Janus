from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

class ActionType(StrEnum):
    MESSAGE = "message"
    TOOL_CALL = "tool_call"
    PROMPT = "prompt"

class Action(BaseModel):
    action_id: str
    session_id: str

    actor_id: str
    target_id: str

    action_type: ActionType
    payload: dict = Field  (default_factory=dict) #TODO

    created_at: datetime = Field(default_factory=datetime.utcnow)

