from abc import abstractmethod
from llmmemory import LlmMemory


class PersistableMemory(LlmMemory):

    @abstractmethod
    def save(self):
        pass
