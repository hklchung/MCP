from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from agents.brief_agent import collect_brief, validate_brief
from agents.content_agent import ContentAgent
from agents.approval_agent import approve, load_guardrails

load_dotenv()

GUARDRAILS_PATH = Path("data/guardrails.txt")

# Track which page is currently active
if "page" not in st.session_state:
    st.session_state.page = "home"


def home_page() -> None:
    st.title("MCP Demo")
    with st.form("brief_form"):
        title = st.text_input("Article Title")
        description = st.text_area("Description", height=200)
        keywords = st.text_input("Keywords")
        model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4o"])
        submitted = st.form_submit_button("Generate")

    if st.button("Guardrails"):
        st.session_state.page = "guardrails"
        st.rerun()

    if submitted:
        form_data = {"title": title, "description": description, "keywords": keywords}
        brief = collect_brief(form_data)
        valid, prompts = validate_brief(brief)
        if not valid:
            for msg in prompts:
                st.warning(msg)
            return
        with st.spinner("Generating draft..."):
            agent = ContentAgent(os.environ.get("OPENAI_API_KEY", ""), model)
            draft = agent.generate_draft(brief)
            guardrails = load_guardrails(GUARDRAILS_PATH)
            ok, feedback = approve(draft, guardrails)

        st.session_state.draft = draft
        st.session_state.approved = ok
        st.session_state.feedback = feedback
        st.session_state.page = "result"
        st.rerun()


def guardrails_page() -> None:
    st.title("Edit Guardrails")
    content = GUARDRAILS_PATH.read_text(encoding="utf-8")
    rules = st.text_area("Rules", content, height=200)

    col1, col2 = st.columns(2)
    if col1.button("Save"):
        GUARDRAILS_PATH.write_text(rules, encoding="utf-8")
        st.success("Saved")
    if col2.button("Back"):
        st.session_state.page = "home"
        st.rerun()


def result_page() -> None:
    st.title("Draft")
    st.text_area("Draft", st.session_state.get("draft", ""), height=300)

    if st.session_state.get("approved"):
        st.success("Status: Approved")
    else:
        st.error(f"Status: Rejected - {st.session_state.get('feedback', '')}")

    if st.button("Back"):
        st.session_state.page = "home"
        st.rerun()


if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "guardrails":
    guardrails_page()
else:
    result_page()
