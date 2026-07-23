"""
groq_client.py

Thin wrapper around the Groq API. Responsible for:
  - creating a client from a user-supplied (BYOK) API key
  - routing each request to the appropriate model (standard vs heavy)
  - sending chat completions
  - parsing token usage from the API response and updating running totals

This module intentionally avoids importing Streamlit directly. Functions
that "update state" accept any mutable mapping (session_state behaves
like one), so this module stays reusable outside of a Streamlit context.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from groq import Groq

from config import MODEL_HEAVY, MODEL_STANDARD, SYSTEM_PROMPT

# Keywords that suggest a request needs the heavier reasoning model rather
# than the fast/general model. This is a lightweight heuristic, not a
# classifier -- it errs toward the cheaper model unless there's a clear
# signal of coding or logic complexity.
_HEAVY_SIGNAL_KEYWORDS = (
    "algorithm", "refactor", "recursion", "recursive", "optimize",
    "optimise", "architecture", "concurrency", "multithread", "async",
    "database", "schema", "regex", "complexity", "big o", "debug",
    "traceback", "stack trace", "unit test", "edge case", "class ",
    "inheritance", "design pattern", "data structure", "compile",
    "race condition", "deadlock", "memory leak", "performance",
    "algorithmic", "state machine", "api integration",
)

# Prompts longer than this are assumed to carry enough detail/complexity
# to warrant the heavier model, even without a keyword match.
_MIN_HEAVY_PROMPT_LENGTH = 400  # characters


@dataclass
class ChatResult:
    """Result of a single chat completion call."""

    content: str
    total_tokens: int
    model_used: str


class GroqClientError(RuntimeError):
    """Raised when client setup or a Groq API call fails."""


def create_client(api_key: str) -> Groq:
    """Instantiate a Groq client from a user-supplied API key."""
    if not api_key or not api_key.strip():
        raise GroqClientError("A Groq API key is required.")
    return Groq(api_key=api_key.strip())


def route_model(prompt: str) -> str:
    """
    Decide which model should handle a given prompt.

    Returns MODEL_HEAVY when the prompt shows signals of non-trivial
    coding or logic work (an embedded code fence, a complexity keyword,
    or simply a long/detailed prompt). Otherwise returns MODEL_STANDARD
    for fast, general chat.
    """
    if not prompt:
        return MODEL_STANDARD

    if "```" in prompt:
        return MODEL_HEAVY

    lowered = prompt.lower()
    if any(keyword in lowered for keyword in _HEAVY_SIGNAL_KEYWORDS):
        return MODEL_HEAVY

    if len(prompt) >= _MIN_HEAVY_PROMPT_LENGTH:
        return MODEL_HEAVY

    return MODEL_STANDARD


def send_chat_completion(
    client: Groq,
    history: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.3,
) -> ChatResult:
    """
    Send a chat completion request to Groq.

    `history` is a list of {"role": ..., "content": ...} dicts for the
    user/assistant turns only -- the system prompt is injected here, not
    stored in session history. If `model` is omitted, it is chosen
    automatically via route_model() based on the most recent user message.
    """
    if model is None:
        last_user_message = next(
            (m["content"] for m in reversed(history) if m.get("role") == "user"),
            "",
        )
        model = route_model(last_user_message)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}, *history]

    try:
        response = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature,
        )
    except Exception as exc:  # the Groq SDK can raise several exception types
        raise GroqClientError(str(exc)) from exc

    content = response.choices[0].message.content

    total_tokens = 0
    usage = getattr(response, "usage", None)
    if usage is not None:
        total_tokens = getattr(usage, "total_tokens", 0) or 0

    return ChatResult(content=content, total_tokens=total_tokens, model_used=model)


def update_token_usage(session_state, result: ChatResult) -> int:
    """
    Add the tokens consumed by `result` to the running total stored at
    session_state["tokens_used"]. Accepts any mutable mapping (such as
    st.session_state), so this module has no direct Streamlit dependency.
    Returns the new running total.
    """
    current = session_state.get("tokens_used", 0)
    updated = current + result.total_tokens
    session_state["tokens_used"] = updated
    return updated