import asyncio

from ceo_assistant.application.pipeline import MessageProcessingPipeline
from ceo_assistant.config import settings
from ceo_assistant.infrastructure.llm.mock_client import MockLLMProcessor
from ceo_assistant.infrastructure.llm.openai_client import OpenAILLMProcessor
from ceo_assistant.infrastructure.telegram.bot import build_app


def build_pipeline() -> MessageProcessingPipeline:
    if settings.use_mock_llm:
        llm = MockLLMProcessor()
    else:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required unless USE_MOCK_LLM=true")
        llm = OpenAILLMProcessor(api_key=settings.openai_api_key, model=settings.openai_model)
    return MessageProcessingPipeline(llm_processor=llm)


async def run() -> None:
    pipeline = build_pipeline()
    app = build_app(settings.telegram_bot_token, pipeline)
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
