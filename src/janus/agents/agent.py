from abc import ABC, abstractmethod

from janus.domain.agent_state import AgentState, AgentStatus


class Agent(ABC):
    def __init__(self, 
                agent_id: str,
                ) -> None:
        self.state = AgentState(
            agent_id=agent_id,
            status=AgentStatus.IDLE,
        )

    @abstractmethod
    def start(self) -> None:
        ...

    @abstractmethod
    def stop(self) -> None:
        ...