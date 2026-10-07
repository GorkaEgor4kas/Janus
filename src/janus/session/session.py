from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

class SessionStatus(StrEnum):
    CREATED = "created"
    INITIALIZED = "initialized"
    READY = "ready"
    RUNNING = "running"
    STOPPING = "stopping"
    FINISHED = "finished"
    ERROR = "error"

class SessionConfig(BaseModel):
    target_config: dict = Field(default_factory=dict)
    red_config: dict = Field(default_factory=dict)
    blue_config: dict = Field(default_factory=dict)
    sandbox_profile: dict = Field(default_factory=dict)
    attack_goal: str
    max_steps: int 

class Session(BaseModel):
    session_id: str
    status: SessionStatus = SessionStatus.CREATED

    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: datetime | None = None
    finished_at: datetime | None = None

    target_id: str
    blue_id: str
    red_id: str

    config: SessionConfig = Field(default_factory=SessionConfig)