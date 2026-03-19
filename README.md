# Gurov AI CEO Bot (MVP)

Telegram-first AI executive assistant MVP with clean architecture and structured outputs.

## MVP Scope

- Input channel: Telegram text messages only
- Input classes: `task`, `reply`, `note`, `document`
- Output types:
  - concise summary
  - draft reply (when relevant)
  - structured task extraction
- Safety: no automatic external actions; confirmation-first behavior

## Architecture (MVP)

- `domain`: business models and boundaries
- `application`: message processing orchestration and output formatting
- `infrastructure`: adapters (Telegram and LLM provider)

Core separation:
- raw input: `IncomingMessage`
- actionable tasks: `ActionableTask`
- knowledge items: `KnowledgeItem`

## Quick Start

1. Create virtual env and install:
   - `python -m venv .venv`
   - `source .venv/bin/activate`
   - `pip install -e ".[dev]"`
2. Configure env:
   - `cp .env.example .env`
   - set `TELEGRAM_BOT_TOKEN`
   - set `OPENAI_API_KEY` or `USE_MOCK_LLM=true`
3. Run:
   - `python -m ceo_assistant.main`

## Suggested v1 Steps

1. Phase 1 (done in this repo): base architecture + pipeline + Telegram adapter
2. Phase 2: better prompts + business test dataset + quality checks
3. Phase 3: persistence layer (events/artifacts), basic review UI/commands
4. Phase 4: selective integrations (tasks, Obsidian, email, meetings, monitoring)
