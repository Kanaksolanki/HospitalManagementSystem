"""
Thin shared wrapper around the Anthropic API, used by report_summarizer.py and
patient_history_summarizer.py for the narrative-generation half of the hybrid
approach (structured/rule-based extraction is done separately in each module).

Requires ANTHROPIC_API_KEY to be set in the environment (e.g. via a .env file
loaded by python-dotenv, same pattern as the Django backend's settings.py).

If no API key is available, `get_narrative()` returns None so callers can fall
back to a rule-based-only summary instead of crashing — important since this
module is meant to be testable standalone, without any keys configured.
"""

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # pragma: no cover - dotenv is a light convenience, not a hard requirement
    pass

try:
    import anthropic
except ImportError:  # pragma: no cover - handled gracefully at call time
    anthropic = None

MODEL = "claude-sonnet-5"

_client = None


def _get_client():
    global _client
    if _client is None and anthropic is not None and os.getenv("ANTHROPIC_API_KEY"):
        _client = anthropic.Anthropic()
    return _client


def get_narrative(system_prompt: str, user_prompt: str, max_tokens: int = 500) -> str | None:
    """Call Claude for a narrative response. Returns None (never raises) if the
    API key is missing or the call fails, so callers can degrade gracefully."""
    client = _get_client()
    if client is None:
        return None
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text_blocks = [b.text for b in response.content if b.type == "text"]
        return "\n".join(text_blocks).strip() or None
    except Exception as exc:  # noqa: BLE001 - degrade gracefully in a demo/MVP context
        print(f"[claude_client] Claude API call failed, falling back to rule-based only: {exc}")
        return None
