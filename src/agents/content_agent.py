from __future__ import annotations

import openai
import requests


class ContentAgent:
    def __init__(self, api_key: str, model: str) -> None:
        openai.api_key = api_key
        self.model = model

    def _fetch_trending_keywords(self, topic: str) -> list[str]:
        """Return a list of trending keywords for the given topic."""
        try:
            resp = requests.get(
                "https://api.datamuse.com/words",
                params={"ml": topic, "max": 5},
                timeout=5,
            )
            resp.raise_for_status()
            return [w.get("word", "") for w in resp.json()]
        except Exception:
            return []

    def fetch_trending_keywords(self, topic: str) -> list[str]:
        return self._fetch_trending_keywords(topic)

    def generate_draft(self, brief: dict, trending: list[str] | None = None) -> str:
        trending = trending or []
        all_keywords = ", ".join([kw for kw in [brief.get("keywords", "")] + trending if kw])
        prompt = (
            f"Write a blog post titled '{brief['title']}' about {brief['description']}.\n"
            f"Include the keywords: {all_keywords}."
        )
        response = openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
