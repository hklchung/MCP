from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for

from agents.brief_agent import collect_brief
from agents.content_agent import ContentAgent
from agents.approval_agent import approve, load_guardrails

load_dotenv()

app = Flask(__name__)
GUARDRAILS_PATH = Path("data/guardrails.txt")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        model = request.form.get("model", "gpt-3.5-turbo")
        brief = collect_brief(request.form)
        agent = ContentAgent(os.environ.get("OPENAI_API_KEY", ""), model)
        draft = agent.generate_draft(brief)
        guardrails = load_guardrails(GUARDRAILS_PATH)
        ok, feedback = approve(draft, guardrails)
        return render_template(
            "result.html", draft=draft, approved=ok, feedback=feedback
        )
    return render_template("index.html")


@app.route("/guardrails", methods=["GET", "POST"])
def edit_guardrails():
    if request.method == "POST":
        lines = request.form.get("rules", "").splitlines()
        GUARDRAILS_PATH.write_text("\n".join(lines), encoding="utf-8")
        return redirect(url_for("edit_guardrails"))
    content = GUARDRAILS_PATH.read_text(encoding="utf-8")
    return render_template("guardrails.html", rules=content)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
