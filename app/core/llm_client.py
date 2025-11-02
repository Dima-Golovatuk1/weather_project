from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    async def generate(self):
        pass



