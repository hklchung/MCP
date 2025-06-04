from __future__ import annotations

def collect_brief(form_data: dict) -> tuple[dict | None, str | None]:
    """Validate form input and return brief data or a follow-up question."""
    title = form_data.get("title", "").strip()
    keywords = form_data.get("keywords", "").strip()
    description = form_data.get("description", "").strip()

    if len(description) < 30:
        return None, "Could you provide more detail in the description?"

    return {
        "title": title,
        "keywords": keywords,
        "description": description,
    }, None
