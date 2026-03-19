import pytest

from ceo_assistant.application.pipeline import MessageProcessingPipeline
from ceo_assistant.domain.models import IncomingMessage, InputType
from ceo_assistant.infrastructure.llm.mock_client import MockLLMProcessor


@pytest.mark.asyncio
async def test_task_message_classification() -> None:
    pipeline = MessageProcessingPipeline(llm_processor=MockLLMProcessor())
    artifact = await pipeline.process(
        IncomingMessage(
            user_id="u1",
            chat_id="c1",
            message_id="m1",
            text="Сделай задачу: подготовить повестку к пятнице",
        )
    )
    assert artifact.classification.input_type == InputType.task
    assert artifact.bot_response.tasks
    assert artifact.bot_response.requires_confirmation is True


@pytest.mark.asyncio
async def test_reply_message_returns_draft() -> None:
    pipeline = MessageProcessingPipeline(llm_processor=MockLLMProcessor())
    artifact = await pipeline.process(
        IncomingMessage(
            user_id="u1",
            chat_id="c1",
            message_id="m2",
            text="Нужно ответить клиенту по срокам релиза",
        )
    )
    assert artifact.classification.input_type == InputType.reply
    assert artifact.bot_response.draft_reply is not None
