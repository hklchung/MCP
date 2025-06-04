from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
import pandas as pd

from agents.brief_agent import collect_brief
from agents.content_agent import ContentAgent
from agents.approval_agent import approve, load_guardrails

import time

load_dotenv()

GUARDRAILS_PATH = Path("data/guardrails.txt")

# Track which page is currently active
if "page" not in st.session_state:
    st.session_state.page = "home"
if "logs" not in st.session_state:
    st.session_state.logs = []
if "trending" not in st.session_state:
    st.session_state.trending = []


def _log(job: str, agent: str, start: float) -> None:
    st.session_state.logs.append(
        {
            "job": job,
            "agent": agent,
            "time": round(time.perf_counter() - start, 1),
            "status": "done",
        }
    )


def home_page() -> None:
    st.title("MCP Demo")
    if st.session_state.get("brief_request"):
        st.info(f"Brief Agent: {st.session_state.brief_request}")
    with st.form("brief_form"):
        title = st.text_input(
            "Article Title",
            value=st.session_state.get("title", ""),
        )
        description = st.text_area(
            "Description",
            height=200,
            value=st.session_state.get("description", ""),
        )
        keywords = st.text_input(
            "Keywords",
            value=st.session_state.get("keywords", ""),
        )
        model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4o"])
        submitted = st.form_submit_button("Generate" if not st.session_state.get("brief_request") else "Continue")

    if st.button("Guardrails"):
        st.session_state.page = "guardrails"
        st.rerun()

    if submitted:
        form_data = {"title": title, "description": description, "keywords": keywords}
        start = time.perf_counter()
        brief, question = collect_brief(form_data)
        _log("Review user requirements", "brief agent", start)

        if question:
            _log("Ask for more information", "brief agent", time.perf_counter())
            st.session_state.brief_request = question
            st.session_state.title = title
            st.session_state.description = description
            st.session_state.keywords = keywords
            st.rerun()
        else:
            st.session_state.brief_request = None
            agent = ContentAgent(os.environ.get("OPENAI_API_KEY", ""), model)
            with st.spinner("Generating draft..."):
                start = time.perf_counter()
                trending = agent.fetch_trending_keywords(
                    brief.get("title") or brief.get("description", "")
                )
                _log(
                    "Look up relevant trending keywords",
                    "content agent",
                    start,
                )
                st.session_state.trending = trending
                start = time.perf_counter()
                draft = agent.generate_draft(brief, trending)
                _log("Draft article", "content agent", start)

                start = time.perf_counter()
                guardrails = load_guardrails(GUARDRAILS_PATH)
                ok, feedback = approve(draft, guardrails)
                _log("Review draft", "approval agent", start)
                if ok:
                    _log("Approved draft", "approval agent", time.perf_counter())
                else:
                    _log(
                        "Raise revision request",
                        "approval agent",
                        time.perf_counter(),
                    )

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
    tabs = st.tabs(["Draft", "Logs"])
    with tabs[0]:
        st.text_area("Draft", st.session_state.get("draft", ""), height=300)

        if st.session_state.get("approved"):
            st.success("Status: Approved")
        else:
            st.error(f"Status: Rejected - {st.session_state.get('feedback', '')}")

        if st.session_state.get("trending"):
            st.markdown("#### Trending Keywords")
            st.write(", ".join(st.session_state.trending))

    with tabs[1]:
        if st.session_state.logs:
            df = pd.DataFrame(st.session_state.logs)
            st.table(df)
        else:
            st.info("No logs yet.")

    if st.button("Back"):
        st.session_state.page = "home"
        st.session_state.trending = []
        st.rerun()


if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "guardrails":
    guardrails_page()
else:
    result_page()
