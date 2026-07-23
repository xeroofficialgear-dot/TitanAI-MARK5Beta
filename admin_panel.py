"""
admin_panel.py

Renders the Task Manager admin view: session metrics, operational logs,
background task queue, and the recent prompt queue. This is a pure
rendering module -- it reads from session state but never mutates
application logic itself.
"""

import streamlit as st

from config import DAILY_TOKEN_LIMIT


def render_admin_panel(session_state) -> None:
    """Render the full Task Manager view into the current Streamlit page."""
    st.title("Task Manager")
    st.caption("Session diagnostics and operational status.")

    st.divider()
    _render_session_metrics(session_state)

    st.divider()
    _render_operational_logs(session_state)

    st.divider()
    _render_background_tasks(session_state)

    st.divider()
    _render_prompt_queue(session_state)


def _render_session_metrics(session_state) -> None:
    st.subheader("Session Metrics")

    tokens_used = session_state.get("tokens_used", 0)
    tokens_remaining = max(0, DAILY_TOKEN_LIMIT - tokens_used)
    request_count = session_state.get("request_count", 0)
    heavy_calls = session_state.get("heavy_model_calls", 0)
    standard_calls = session_state.get("standard_model_calls", 0)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tokens used", f"{tokens_used:,}")
    col2.metric("Tokens remaining", f"{tokens_remaining:,}")
    col3.metric("Requests sent", request_count)
    col4.metric("Heavy model calls", heavy_calls)

    usage_ratio = min(1.0, tokens_used / DAILY_TOKEN_LIMIT) if DAILY_TOKEN_LIMIT else 0.0
    st.progress(usage_ratio, text=f"{tokens_used:,} / {DAILY_TOKEN_LIMIT:,} daily tokens")

    st.caption(f"Standard model calls: {standard_calls}  |  Heavy model calls: {heavy_calls}")


def _render_operational_logs(session_state) -> None:
    st.subheader("Operational Logs")
    logs = session_state.get("task_logs", [])
    if not logs:
        st.write("No log entries yet.")
        return

    log_text = "\n".join(
        f"[{i + 1}] {entry}" for i, entry in enumerate(reversed(logs))
    )
    st.text_area(
        "Recent activity",
        value=log_text,
        height=180,
        disabled=True,
        label_visibility="collapsed",
    )


def _render_background_tasks(session_state) -> None:
    st.subheader("Background Tasks")
    tasks = session_state.get("background_tasks", [])
    if not tasks:
        st.write("No background tasks queued.")
        return

    for task in tasks:
        label = task.get("label", "Unnamed task")
        status = task.get("status", "pending")
        st.write(f"- **{label}** -- {status}")


def _render_prompt_queue(session_state) -> None:
    st.subheader("Prompt Queue")
    prompt_queue = session_state.get("prompt_queue", [])
    if not prompt_queue:
        st.write("No prompts queued.")
        return

    recent = prompt_queue[-10:]
    for i, prompt in enumerate(recent, start=1):
        preview = prompt if len(prompt) <= 120 else prompt[:117] + "..."
        st.write(f"{i}. {preview}")