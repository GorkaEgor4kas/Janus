from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, Field

class EnforcementResultType(StrEnum):
    ALLOWED = "allowed"
    BLOCKED = "blocked"

class EnforcementResult(BaseModel):
    enfrocement_id: str
    action_id: str
    session_id: str

    result: EnforcementResultType
    reason: str

    created_at: datetime = Field(default_factory=datetime.utcnow)


