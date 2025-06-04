from __future__ import annotations

import openai


class ContentAgent:
    def __init__(self, api_key: str, model: str) -> None:
        openai.api_key = api_key
        self.model = model

    def generate_draft(self, brief: dict) -> str:
        prompt = (
            f"Write a blog post titled '{brief['title']}' about {brief['description']}.\n"
            f"Include the keywords: {brief['keywords']}."
        )
        response = openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
