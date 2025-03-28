from abc import ABC, abstractmethod

from agent_response import AgentResponse


class Agent(ABC):

    @abstractmethod
    def invoke(self, query) -> AgentResponse:
        pass