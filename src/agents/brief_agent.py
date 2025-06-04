def collect_brief(form_data: dict) -> dict:
    """Return collected brief data."""
    return {
        "title": form_data.get("title", ""),
        "keywords": form_data.get("keywords", ""),
        "description": form_data.get("description", ""),
    }


def validate_brief(brief: dict) -> tuple[bool, list[str]]:
    """Check that all required fields are present.

    Parameters
    ----------
    brief:
        Dictionary containing the collected brief data.

    Returns
    -------
    tuple[bool, list[str]]
        A tuple where the first element indicates if the brief is valid and the
        second element is a list of prompts for any missing fields.
    """

    required_prompts = {
        "title": "Please provide an article title.",
        "description": "Please add a short description of the article.",
        "keywords": "Please specify keywords for the article.",
    }

    prompts = [
        message
        for field, message in required_prompts.items()
        if not brief.get(field, "").strip()
    ]
    return len(prompts) == 0, prompts
