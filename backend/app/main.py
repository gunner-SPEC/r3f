import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

from . import llm
from . import assembler

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

@app.post('/generate_and_assemble')
async def generate_and_assemble(req: PromptRequest):
    """Generate a manifest from the prompt and assemble it into a zip artifact.

    Returns: {ok: True, artifact: {project_name, output_dir, zip_path}}
    """
    prompt = req.prompt
    manifest = await llm.generate_manifest(prompt)
    result = assembler.assemble_manifest(manifest)
    return {"ok": True, "artifact": result}
