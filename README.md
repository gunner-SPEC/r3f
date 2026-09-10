# r3f — AI Game Maker (MVP scaffold)

This repository contains a minimal scaffold for the "talk-to-create" game-maker app MVP: a simple web frontend and a FastAPI backend that accept a prompt and return a generated project stub. This scaffold is intended to help iterate on prompt parsing, project assembly, and build orchestration before adding real LLM/asset/build integrations.

What's included
- backend/: FastAPI backend with a stubbed /generate endpoint
- frontend/: static single-page UI (index.html) that sends prompts to the backend
- docs/: architecture notes and next steps

Quickstart (development)
1. Start the backend
   - python3 -m venv .venv && source .venv/bin/activate
   - pip install -r backend/requirements.txt
   - uvicorn backend.app.main:app --reload --port 8000

2. Open the frontend
   - Open frontend/index.html in your browser (or serve it with a static server)

3. Try a prompt in the UI and inspect backend logs

Next steps
- Hook a real LLM to backend.generate() and implement project template assembly
- Add engine templates (Unity/Godot) and a build worker
- Implement asset generation and caching
