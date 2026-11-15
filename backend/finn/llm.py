"""Thin OpenAI-compatible client with on-disk caching and two-tier model routing.
cheap: bulk extraction / short summaries. strong: reasoning over research. Optional: app degrades to rules."""
import hashlib
import json

import requests

from .config import CACHE, LLM_BASE, LLM_CHEAP, LLM_KEY, LLM_STRONG


def available() -> bool:
    return bool(LLM_KEY)


def chat(tier: str, system: str, user: str, max_tokens: int = 700) -> str | None:
    if not LLM_KEY:
        return None
    model = LLM_STRONG if tier == "strong" else LLM_CHEAP
    key = hashlib.sha1(f"{model}|{system}|{user}".encode()).hexdigest()
    p = CACHE / f"llm_{key}.json"
    if p.exists():
        return json.loads(p.read_text())["out"]
    try:
        r = requests.post(
            f"{LLM_BASE}/chat/completions",
            headers={"Authorization": f"Bearer {LLM_KEY}"},
            json={"model": model, "max_tokens": max_tokens, "temperature": 0.2,
                  "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]},
            timeout=60,
        )
        r.raise_for_status()
        out = r.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        return None
    p.write_text(json.dumps({"out": out}))
    return out
