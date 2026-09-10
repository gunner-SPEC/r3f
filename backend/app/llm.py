"""
LLM helper for r3f backend.

Behavior:
- If OPENAI_API_KEY is provided in the environment, this module will call OpenAI's ChatCompletion API
  (via the openai python package) to ask the model to produce a JSON manifest describing a generated
  game project. The model is instructed to output only JSON following a simple schema.
- If OPENAI_API_KEY is missing, the module returns a deterministic stub manifest so the app remains
  usable locally without credentials.

Environment variables:
- OPENAI_API_KEY: API key for OpenAI-compatible provider
- OPENAI_MODEL: (optional) model name to use, default: gpt-4o-mini
"""
import os
import json
import re
from typing import Dict, Any

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# only import openai if key is present to avoid hard dependency at runtime in the stub case
if OPENAI_API_KEY:
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
    except Exception:
        openai = None
else:
    openai = None


async def generate_manifest(prompt: str) -> Dict[str, Any]:
    """Return a manifest dict describing a generated game project.

    The manifest schema (expected):
    {
      "project_name": "...",
      "template": "2D-platformer" | "3D-fps" | ...,
      "description": "short description",
      "files": [{"path": "", "type":"scene|script|asset", "contents": "optional file contents"}, ...]
    }
    """
    if not OPENAI_API_KEY or openai is None:
        # Return a deterministic stub so local testing works without credentials
        return {
            "project_name": "generated-game-stub",
            "template": "2D-platformer",
            "description": "Stubbed manifest because OPENAI_API_KEY is not set.",
            "prompt_received": prompt,
            "files": [
                {"path": "game/main.scene", "type": "scene", "note": "placeholder scene"},
                {"path": "game/player.cs", "type": "script", "note": "placeholder script"}
            ]
        }

    system = (
        "You are a game project manifest generator.\n"
        "Given a user's free-form prompt describing a game, output a JSON object and ONLY the JSON object (no surrounding text).\n"
        "The JSON must follow this schema:\n"
        "{\n"
        "  \"project_name\": string,\n"
        "  \"template\": string,          (e.g., \"2D-platformer\" or \"3D-fps\")\n"
        "  \"description\": string,\n"
        "  \"files\": [\n"
        "     { \"path\": string, \"type\": string, \"contents\": string (optional) }\n"
        "  ]\n"
        "}\n"
        "Keep descriptions short. For any code in files.contents, keep examples small (<=200 lines)."
    )

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"User prompt: {prompt}"}
    ]

    try:
        resp = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.2,
            max_tokens=800,
        )
        text = resp.choices[0].message.content
    except Exception as e:
        return {
            "project_name": "generated-game-error",
            "template": "error",
            "description": f"LLM call failed: {e}",
            "prompt_received": prompt,
            "files": []
        }

    # Extract JSON blob from response text
    text = text.strip()
    try:
        manifest = json.loads(text)
        return manifest
    except json.JSONDecodeError:
        # Attempt to pull the first JSON object substring
        m = re.search(r"\{[\s\S]*\}", text)
        if m:
            try:
                manifest = json.loads(m.group(0))
                return manifest
            except json.JSONDecodeError:
                pass
        # Fallback: return a helpful error wrapper
        return {
            "project_name": "generated-game-parse-error",
            "template": "unknown",
            "description": "Could not parse JSON from model response.",
            "raw_model_output": text,
            "prompt_received": prompt,
            "files": []
        }
