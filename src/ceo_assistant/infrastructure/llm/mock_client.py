from ceo_assistant.domain.models import (
    ActionableTask,
    BotStructuredResponse,
    ClassificationResult,
    IncomingMessage,
    InputType,
    KnowledgeItem,
    ProcessingArtifact,
)
from ceo_assistant.infrastructure.llm.base import LLMProcessor


class MockLLMProcessor(LLMProcessor):
    async def analyze_message(self, message: IncomingMessage) -> ProcessingArtifact:
        text = message.text.lower()

        if any(word in text for word in ["ответь", "ответить", "reply", "respond"]):
            input_type = InputType.reply
        elif any(word in text for word in ["задача", "todo", "сделай", "task"]):
            input_type = InputType.task
        elif len(message.text) > 600:
            input_type = InputType.document
        else:
            input_type = InputType.note

        tasks = []
        draft_reply = None
        knowledge_items = []

        if input_type == InputType.task:
            tasks.append(
                ActionableTask(
                    title="Review and execute request",
                    details=message.text[:220],
                    priority="medium",
                )
            )
        elif input_type == InputType.reply:
            draft_reply = (
                "Thanks for the message. I reviewed it and will return with a concise update shortly."
            )
        else:
            knowledge_items.append(
                KnowledgeItem(
                    title="Captured note",
                    content=message.text[:280],
                    tags=["mvp", input_type.value],
                )
            )

        classification = ClassificationResult(
            input_type=input_type,
            confidence=0.72,
            rationale="Keyword and length-based fallback classification (mock mode).",
        )

        bot_response = BotStructuredResponse(
            input_type=input_type,
            summary=message.text[:240],
            draft_reply=draft_reply,
            tasks=tasks,
            knowledge_items=knowledge_items,
            requires_confirmation=True,
        )

        return ProcessingArtifact(
            raw_input=message,
            classification=classification,
            actionable_tasks=tasks,
            knowledge_items=knowledge_items,
            bot_response=bot_response,
        )
