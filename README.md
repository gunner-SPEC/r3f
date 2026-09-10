Updated README: artifact endpoints

New endpoints
- GET /artifacts
  Returns a JSON list of available zip artifacts produced by /generate_and_assemble. Each entry contains name, path, size (bytes) and modified (unix timestamp).

- GET /artifacts/{zip_name}
  Downloads the named zip artifact as an attachment. Example:

  curl -O http://localhost:8000/artifacts/generated-game-stub.zip

Usage notes
- Artifacts are stored under backend/generated/ by default. In production you should serve artifacts from object storage (S3) and return signed URLs instead of serving files directly from the app.
- To enable automatic pruning of old artifacts set ARTIFACT_RETENTION_DAYS in the environment (integer days). If set to 0 or omitted, no pruning is performed.

