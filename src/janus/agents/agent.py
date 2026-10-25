from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class Agent(ABC):
    def __init__(self, agent_id: str):
        self.agent_id = agent_id


    @abstractmethod
    def start(self) -> None:
        ...

    @abstractmethod
    def stop(self) -> None:
        ...

    def handle(self, input: Any) -> Any:
        ...


    