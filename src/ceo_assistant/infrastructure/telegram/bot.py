from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from ceo_assistant.application.pipeline import MessageProcessingPipeline
from ceo_assistant.application.response_formatter import format_response_for_telegram
from ceo_assistant.domain.models import IncomingMessage


async def _start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if not update.message:
        return
    await update.message.reply_text(
        "AI CEO Assistant MVP is running.\nSend any text message and I will classify it."
    )


async def _handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text or not update.effective_chat:
        return

    pipeline: MessageProcessingPipeline = context.application.bot_data["pipeline"]
    msg = update.message
    artifact = await pipeline.process(
        IncomingMessage(
            user_id=str(msg.from_user.id) if msg.from_user else "unknown",
            chat_id=str(update.effective_chat.id),
            message_id=str(msg.message_id),
            text=msg.text,
        )
    )
    formatted = format_response_for_telegram(artifact.bot_response)
    await msg.reply_text(formatted)


def build_app(token: str, pipeline: MessageProcessingPipeline) -> Application:
    app = Application.builder().token(token).build()
    app.bot_data["pipeline"] = pipeline
    app.add_handler(CommandHandler("start", _start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, _handle_text))
    return app
