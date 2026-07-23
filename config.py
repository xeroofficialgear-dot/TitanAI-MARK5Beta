"""
config.py

Central configuration for the Titan chat application. Holds constants,
model identifiers, and the base system prompt. This module has no
Streamlit or network dependencies, so it can be imported anywhere
without side effects.
"""

# --- Usage limits -----------------------------------------------------------
DAILY_TOKEN_LIMIT = 30000

# --- Model identifiers --------------------------------------------------------
# Fast, low-cost model used for general chat and simple requests.
MODEL_STANDARD = "llama-3.1-8b-instant"

# Larger model reserved for complex coding, debugging, and multi-step
# reasoning tasks, where answer quality matters more than latency.
MODEL_HEAVY = "llama-3.3-70b-versatile"

# --- System prompt -------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are a precise, code-first technical assistant. "
    "Answer directly and concisely. "
    "When the user asks for code, respond primarily with a single, complete, "
    "correct code block and minimal surrounding commentary. "
    "Do not pad responses with greetings, apologies, filler phrases, or "
    "restatements of the question. "
    "If a request is ambiguous, make a reasonable assumption, state it in one "
    "short line, and proceed rather than asking a clarifying question. "
    "Prefer working, runnable code over pseudocode or partial snippets."
)