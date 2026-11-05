from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, Field


class ResultStatus(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"
    BLOCKED = "blocked"


class ActionResult(BaseModel):
    result_id: str
    action_id: str
    session_id: str

    status: ResultStatus
    output: dict = Field(default_factory=dict)
    error: str | None = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
