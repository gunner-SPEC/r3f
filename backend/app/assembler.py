import os
import shutil
import tempfile
from pathlib import Path
import zipfile
from typing import Dict, Any

BASE_OUTPUT = Path(__file__).resolve().parents[1] / "generated"
BASE_OUTPUT.mkdir(exist_ok=True)


def assemble_manifest(manifest: Dict[str, Any]) -> Dict[str, Any]:
    """Assemble a manifest into a project folder and zip it.

    Returns a dict with keys: project_name, output_dir, zip_path
    """
    project_name = manifest.get("project_name", "generated-game")
    safe_name = "_".join(project_name.split())
    work_dir = BASE_OUTPUT / safe_name

    # remove existing dir if present
    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True)

    files = manifest.get("files", [])
    for f in files:
        path = f.get("path") or f.get("name")
        if not path:
            continue
        dest = work_dir / Path(path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        contents = f.get("contents")
        if contents is None:
            # generate a small placeholder based on type
            ftype = f.get("type", "asset")
            if ftype == "script":
                contents = "// placeholder script file\n// Add your game logic here\n"
            elif ftype == "scene":
                contents = "[gd_scene load_steps=2 format=2]\nnode name=\"Root\" type=Node\n"
            else:
                contents = ""  # empty for assets
        # write file
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(contents)

    # write a simple manifest file
    manifest_path = work_dir / "manifest.json"
    import json

    with open(manifest_path, "w", encoding="utf-8") as mh:
        json.dump(manifest, mh, indent=2)

    # create a zip
    zip_name = f"{safe_name}.zip"
    zip_path = BASE_OUTPUT / zip_name
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in work_dir.rglob("*"):
            if file_path.is_file():
                zf.write(file_path, arcname=str(file_path.relative_to(work_dir)))

    return {"project_name": project_name, "output_dir": str(work_dir), "zip_path": str(zip_path)}
