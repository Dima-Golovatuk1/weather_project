from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    async def generate_al_text(self):
        pass



