def collect_brief(form_data: dict) -> dict:
    """Return collected brief data."""
    return {
        "title": form_data.get("title", ""),
        "keywords": form_data.get("keywords", ""),
        "description": form_data.get("description", ""),
    }
