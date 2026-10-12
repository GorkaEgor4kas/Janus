from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, Field

class EventType(StrEnum):
    SESSION_CREATED = "session_created"
    SESSION_STARTED = "session_started"
    SESSION_STOPED = "session_stopped"
    SESSION_FINISHED = "session_finished"

    COMPONENT_READY = "component_ready"
    COMPONENT_ERROR = "component_error"

    ACTION_REQUESTED = "action_requested"
    SECURITY_DECISION_MADE = "security_decision_made"
    ACTION_BLOCKED = "action_blocked"
    ACTION_ALLOWED = "action_allowed"
    ACTION_EXECUTED = "action_executed"
    ACTION_RESULT_RECEIVED = "action_result_received"

    GOAL_ACHIVED = "goal_achived"
    MAX_STEPS_REACHED = "max_steps_reached"


class Event(BaseModel):
    event_id: str
    session_id: str

    timestamp: datetime = Field(default_factory=datetime.utcnow)

    event_type: EventType
    source: str #TODO

    payload: dict = Field(default_factory=dict)

    