from ceo_assistant.domain.models import IncomingMessage, ProcessingArtifact
from ceo_assistant.infrastructure.llm.base import LLMProcessor


class MessageProcessingPipeline:
    def __init__(self, llm_processor: LLMProcessor) -> None:
        self.llm_processor = llm_processor

    async def process(self, message: IncomingMessage) -> ProcessingArtifact:
        # MVP keeps orchestration thin: one LLM pass + normalized artifact.
        return await self.llm_processor.analyze_message(message)
