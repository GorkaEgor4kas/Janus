from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, Field


class DecisionType(StrEnum):
    ALLOWED = "allowed"
    BLOCKED = "blocked"


class SecurityDecision(BaseModel):
    decision_id: str
    action_id: str
    session_id: str

    decision: DecisionType
    reason: str

    created_at: datetime = Field(default_factory=datetime.utcnow)
