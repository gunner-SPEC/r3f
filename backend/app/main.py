import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

from . import llm

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
    prompt = req.prompt
    manifest = await llm.generate_manifest(prompt)
    return {"ok": True, "manifest": manifest}
