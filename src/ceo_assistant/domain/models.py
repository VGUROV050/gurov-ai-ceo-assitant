from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class InputType(str, Enum):
    task = "task"
    reply = "reply"
    note = "note"
    document = "document"


class IncomingMessage(BaseModel):
    source: Literal["telegram"] = "telegram"
    user_id: str
    chat_id: str
    message_id: str
    text: str
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ActionableTask(BaseModel):
    title: str
    details: str = ""
    priority: Literal["low", "medium", "high"] = "medium"
    due_hint: str | None = None


class KnowledgeItem(BaseModel):
    title: str
    content: str
    tags: list[str] = Field(default_factory=list)


class ClassificationResult(BaseModel):
    input_type: InputType
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str


class BotStructuredResponse(BaseModel):
    input_type: InputType
    summary: str
    draft_reply: str | None = None
    tasks: list[ActionableTask] = Field(default_factory=list)
    knowledge_items: list[KnowledgeItem] = Field(default_factory=list)
    requires_confirmation: bool = True
    safety_notes: list[str] = Field(default_factory=lambda: ["No external actions were executed."])


class ProcessingArtifact(BaseModel):
    raw_input: IncomingMessage
    classification: ClassificationResult
    actionable_tasks: list[ActionableTask] = Field(default_factory=list)
    knowledge_items: list[KnowledgeItem] = Field(default_factory=list)
    bot_response: BotStructuredResponse
