Updated README: added generate_and_assemble API info

This project now includes a simple assembler and a /generate_and_assemble endpoint that will
invoke the LLM (stub or real provider) to create a manifest and then write project files into
backend/generated/<project_name>/ and produce a zip artifact.

Usage (after starting backend):

curl -X POST http://localhost:8000/generate_and_assemble -H "Content-Type: application/json" -d '{"prompt":"Create a small 2D platformer with double jump"}'

The response will include the path to the zip file on the backend host. For local testing you can
then open backend/generated/<project_name>.zip to inspect the assembled project.
