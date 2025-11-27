# Notes Backend (Flask)

Simple REST API for managing text notes with in-memory storage.

Run:
- python run.py (binds to 0.0.0.0:3001)

Endpoints:
- GET /               -> API info
- GET /health         -> { "status": "ok" }
- POST /notes         -> create note {title, content}
- GET /notes          -> list notes
- GET /notes/<id>     -> retrieve note
- PUT /notes/<id>     -> update note (title/content)
- DELETE /notes/<id>  -> delete note

Notes have: id, title, content, created_at, updated_at

CORS: Enabled for all origins.

OpenAPI/Docs:
- Swagger UI: /docs
- OpenAPI JSON: /openapi.json
