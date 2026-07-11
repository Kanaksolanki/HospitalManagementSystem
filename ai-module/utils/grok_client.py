"""
Thin wrapper around Groq's API (OpenAI-compatible, free tier, no card
required). Mirrors claude_client.py's get_narrative() signature so callers
can switch providers without changing their own code.

Returns None if GROQ_API_KEY isn't set or the call fails -- callers must
handle the fallback case themselves, same pattern as claude_client.py.
"""

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


def get_narrative(system_prompt: str, user_prompt: str, max_tokens: int = 400) -> str | None:
    if not GROQ_API_KEY:
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception:
        return None