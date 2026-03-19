from abc import ABC, abstractmethod

from ceo_assistant.domain.models import IncomingMessage, ProcessingArtifact


class LLMProcessor(ABC):
    @abstractmethod
    async def analyze_message(self, message: IncomingMessage) -> ProcessingArtifact:
        """Classify and structure the incoming message."""
