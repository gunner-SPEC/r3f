import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Any, Dict
from datetime import datetime, timedelta

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

# Artifact retention (days). If <= 0, no automatic pruning is performed.
ARTIFACT_RETENTION_DAYS = int(os.getenv("ARTIFACT_RETENTION_DAYS", "0"))

class PromptRequest(BaseModel):
    prompt: str

@app.on_event("startup")
def startup_prune_artifacts():
    if ARTIFACT_RETENTION_DAYS <= 0:
        return
    base = assembler.BASE_OUTPUT
    if not base.exists():
        return
    cutoff = datetime.now() - timedelta(days=ARTIFACT_RETENTION_DAYS)
    removed = 0
    for p in base.glob("*.zip"):
        try:
            mtime = datetime.fromtimestamp(p.stat().st_mtime)
            if mtime < cutoff:
                p.unlink()
                removed += 1
        except Exception:
            continue

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

@app.get('/artifacts')
async def list_artifacts():
    """List available zip artifacts under the assembler output directory."""
    base = assembler.BASE_OUTPUT
    if not base.exists():
        return {"artifacts": []}
    artifacts = []
    for p in sorted(base.glob("*.zip")):
        try:
            st = p.stat()
            artifacts.append({
                "name": p.name,
                "path": f"/artifacts/{p.name}",
                "size": st.st_size,
                "modified": int(st.st_mtime),
            })
        except Exception:
            continue
    return {"artifacts": artifacts}

@app.get('/artifacts/{zip_name}')
async def get_artifact(zip_name: str):
    """Download a named artifact. Validates the name to prevent path traversal."""
    # Basic validation to avoid path traversal
    if ".." in zip_name or zip_name.startswith("/") or zip_name.endswith("/"):
        raise HTTPException(status_code=400, detail="Invalid artifact name")
    file_path = assembler.BASE_OUTPUT / zip_name
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Artifact not found")
    # Serve the file as an attachment
    return FileResponse(str(file_path), media_type="application/zip", filename=zip_name)
