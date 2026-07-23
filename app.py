"""
app.py

Main Streamlit application: a minimalist chat interface backed by Groq,
with a sidebar token tracker, BYOK API key input, and a Task Manager
admin view.
"""

import datetime as dt

import streamlit as st

from admin_panel import render_admin_panel
from config import DAILY_TOKEN_LIMIT, MODEL_HEAVY, MODEL_STANDARD
from groq_client import (
    GroqClientError,
    create_client,
    send_chat_completion,
    update_token_usage,
)

st.set_page_config(page_title="Titan", layout="wide")

# Minimal global styling -- no imagery, no gradients, no decoration.
st.markdown(
    """
    <style>
    .stApp { background-color: #fafafa; }
    section[data-testid="stSidebar"] { background-color: #f2f2f2; }
    </style>
    """,
    unsafe_allow_html=True,
)


def _init_state() -> None:
    defaults = {
        "api_key": "",
        "messages": [],
        "tokens_used": 0,
        "request_count": 0,
        "standard_model_calls": 0,
        "heavy_model_calls": 0,
        "task_logs": [],
        "background_tasks": [
            {"label": "Daily token quota reset", "status": "scheduled"},
        ],
        "prompt_queue": [],
        "show_admin_panel": False,
        "usage_date": dt.date.today().isoformat(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    _reset_daily_usage_if_needed()


def _reset_daily_usage_if_needed() -> None:
    today = dt.date.today().isoformat()
    if st.session_state["usage_date"] == today:
        return

    st.session_state["usage_date"] = today
    st.session_state["tokens_used"] = 0
    st.session_state["request_count"] = 0
    st.session_state["standard_model_calls"] = 0
    st.session_state["heavy_model_calls"] = 0
    st.session_state["task_logs"].append("Daily token counter reset.")


def _log(entry: str) -> None:
    st.session_state["task_logs"].append(entry)


def _render_sidebar() -> None:
    with st.sidebar:
        st.header("Titan")

        st.session_state["api_key"] = st.text_input(
            "Groq API key",
            value=st.session_state["api_key"],
            type="password",
            placeholder="Enter your own Groq API key",
            help="Bring your own key. It is kept only for this session and never stored.",
        )

        st.divider()

        st.subheader("Daily usage")
        tokens_used = st.session_state["tokens_used"]
        ratio = min(1.0, tokens_used / DAILY_TOKEN_LIMIT)
        st.progress(ratio, text=f"{tokens_used:,} / {DAILY_TOKEN_LIMIT:,} tokens")

        if tokens_used >= DAILY_TOKEN_LIMIT:
            st.error("Daily token limit reached. Requests are paused until reset.")
        elif ratio >= 0.9:
            st.warning("Approaching the daily token limit.")

        st.divider()

        st.session_state["show_admin_panel"] = st.toggle(
            "Task Manager view",
            value=st.session_state["show_admin_panel"],
        )

        if st.button("Clear conversation", use_container_width=True):
            st.session_state["messages"] = []
            _log("Conversation cleared.")
            st.rerun()


def _render_chat() -> None:
    st.title("Titan")
    st.caption("Code-first assistant.")

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Message Titan")
    if not prompt:
        return

    if not st.session_state["api_key"].strip():
        st.error("Add your Groq API key in the sidebar to start chatting.")
        return

    if st.session_state["tokens_used"] >= DAILY_TOKEN_LIMIT:
        st.error("Daily token limit reached. Try again after the daily reset.")
        return

    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.session_state["prompt_queue"].append(prompt)
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.write("Working...")
        try:
            client = create_client(st.session_state["api_key"])
            result = send_chat_completion(client, st.session_state["messages"])
            placeholder.write(result.content)

            st.session_state["messages"].append(
                {"role": "assistant", "content": result.content}
            )
            update_token_usage(st.session_state, result)
            st.session_state["request_count"] += 1

            if result.model_used == MODEL_STANDARD:
                st.session_state["standard_model_calls"] += 1
            elif result.model_used == MODEL_HEAVY:
                st.session_state["heavy_model_calls"] += 1

            _log(f"Response generated using {result.model_used} ({result.total_tokens} tokens).")
        except GroqClientError as exc:
            placeholder.error(f"Request failed: {exc}")
            _log(f"Request failed: {exc}")


def main() -> None:
    _init_state()
    _render_sidebar()

    if st.session_state["show_admin_panel"]:
        render_admin_panel(st.session_state)
    else:
        _render_chat()


if __name__ == "__main__":
    main()