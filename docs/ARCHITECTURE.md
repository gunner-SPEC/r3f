Architecture notes

Goal: provide a simple orchestration path from a user's text prompt to a generated game project.

Components
- Frontend (static UI): collect prompts, show results, allow inspection and edits
- Backend (orchestrator): parse prompt, call LLM, assemble project files using templates, run build worker
- Build worker (future): run game engine CLI builds (Unity/Godot) and produce exports
- Storage: object store for assets and builds

MVP scope for this repo
- Local prompt -> manifest flow (stubbed)
- Manual template files to be added later
- Basic UI to iterate on prompts and manifest format

Next steps (concrete)
1. Add LLM integration to backend/app/main.py using your chosen provider
2. Create a `templates/` folder that contains an engine project skeleton for a 2D template
3. Implement a worker service that can run headless builds and return artifacts
4. Add authentication, asset store, and build queue
