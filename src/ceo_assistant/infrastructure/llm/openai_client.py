from __future__ import annotations

import asyncio
import json
from typing import Any

from openai import OpenAI
from pydantic import ValidationError

from ceo_assistant.domain.models import (
    BotStructuredResponse,
    ClassificationResult,
    IncomingMessage,
    ProcessingArtifact,
)
from ceo_assistant.infrastructure.llm.base import LLMProcessor


SYSTEM_PROMPT = """
You are an executive assistant parser for a Telegram MVP.
Your task is to classify incoming text and return a strict JSON object.

Rules:
1) input_type must be one of: task, reply, note, document
2) response must always be structured and concise
3) do not suggest executing external actions automatically
4) requires_confirmation must be true
5) tasks and knowledge_items should be arrays (can be empty)
6) confidence should be between 0 and 1

Return valid JSON only (no markdown, no backticks).

Required schema:
{
  "classification": {
    "input_type": "task|reply|note|document",
    "confidence": 0.0,
    "rationale": "..."
  },
  "bot_response": {
    "input_type": "task|reply|note|document",
    "summary": "...",
    "draft_reply": "..." | null,
    "tasks": [
      {"title": "...", "details": "...", "priority": "low|medium|high", "due_hint": "..." | null}
    ],
    "knowledge_items": [
      {"title": "...", "content": "...", "tags": ["..."]}
    ],
    "requires_confirmation": true,
    "safety_notes": ["No external actions were executed."]
  }
}
""".strip()


def _extract_json(content: str) -> dict[str, Any]:
    stripped = content.strip()
    if stripped.startswith("```") and stripped.endswith("```"):
        stripped = stripped[3:-3].strip()
        if stripped.lower().startswith("json"):
            stripped = stripped[4:].strip()
    if not stripped.startswith("{"):
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start != -1 and end != -1 and end > start:
            stripped = stripped[start : end + 1]
    return json.loads(stripped)


class OpenAILLMProcessor(LLMProcessor):
    def __init__(self, api_key: str, model: str) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    async def analyze_message(self, message: IncomingMessage) -> ProcessingArtifact:
        response = await asyncio.to_thread(
            self.client.chat.completions.create,
            model=self.model,
            temperature=0.2,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Incoming Telegram text:\n"
                        f"{message.text}\n\n"
                        "Now return the JSON object."
                    ),
                },
            ],
        )

        raw_content = response.choices[0].message.content or "{}"
        parsed = _extract_json(raw_content)

        try:
            classification = ClassificationResult.model_validate(parsed["classification"])
            bot_response = BotStructuredResponse.model_validate(parsed["bot_response"])
        except (KeyError, ValidationError) as exc:
            raise ValueError("LLM returned invalid schema payload") from exc

        return ProcessingArtifact(
            raw_input=message,
            classification=classification,
            actionable_tasks=bot_response.tasks,
            knowledge_items=bot_response.knowledge_items,
            bot_response=bot_response,
        )
