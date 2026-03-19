from ceo_assistant.domain.models import BotStructuredResponse


def format_response_for_telegram(response: BotStructuredResponse) -> str:
    lines: list[str] = [
        f"Type: {response.input_type.value}",
        "",
        "Summary:",
        response.summary,
    ]

    if response.draft_reply:
        lines.extend(
            [
                "",
                "Draft reply:",
                response.draft_reply,
            ]
        )

    if response.tasks:
        lines.append("")
        lines.append("Structured tasks:")
        for idx, task in enumerate(response.tasks, start=1):
            due = f" | due: {task.due_hint}" if task.due_hint else ""
            lines.append(
                f"{idx}. {task.title} (priority: {task.priority}){due}\n   {task.details}"
            )

    if response.knowledge_items:
        lines.append("")
        lines.append("Knowledge items:")
        for idx, item in enumerate(response.knowledge_items, start=1):
            tags = f" [{', '.join(item.tags)}]" if item.tags else ""
            lines.append(f"{idx}. {item.title}{tags}\n   {item.content}")

    lines.extend(
        [
            "",
            "Safety:",
            "- External actions are not executed automatically.",
            "- Confirmation is required for sensitive steps.",
        ]
    )

    return "\n".join(lines).strip()
