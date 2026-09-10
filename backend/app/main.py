from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

app = FastAPI(title="r3f - AI Game Maker (backend)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.get('/health')
async def health() -> Dict[str, Any]:
    return {"status": "ok"}

@app.post('/generate')
async def generate(req: PromptRequest):
    # TODO: replace this stub with LLM orchestration and project assembly
    prompt = req.prompt
    # Simple stubbed response: echo plus a minimal project manifest
    manifest = {
        "project_name": "generated-game",
        "template": "2D-platformer",
        "prompt_received": prompt,
        "files": [
            {"path": "game/main.scene", "type": "scene", "note": "placeholder scene"},
            {"path": "game/player.cs", "type": "script", "note": "placeholder script"}
        ]
    }
    return {"ok": True, "manifest": manifest}
