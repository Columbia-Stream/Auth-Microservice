# Auth Microservice

## Overview

This microservice is responsible for managing users. It exposes CRUD-style endpoints (GET/POST/PUT/DELETE) plus a health check, though most endpoints are currently stubbed.

### Features implemented so far

  

---

## Assumptions & Design Decisions

  

---

## Getting Started (Development)

### Prerequisites

- Python 3.10+ (tested on Python 3.12)  
- `venv` (or another virtual environment method)  

### Setup 

```bash
# From project root
python3 -m venv venv
source venv/bin/activate            # macOS/Linux
# venv\Scripts\activate            # Windows (PowerShell)

pip freeze > requirements.txt
```

### Running the service
```bash 
uvicorn main:app --reload --port 8000
```

- Visit http://127.0.0.1:8000/healthz → {"ok": true}
- Visit http://127.0.0.1:8000/docs → Swagger UI where you can test GET /search, POST/PUT/DELETE stubs
- Use Try it out in Swagger to call endpoints
- GET /search?q=Kubernetes should return a mock video matching “Kubernetes Basics”

### Running Tests
```bash 
# Be sure project root is in PYTHONPATH, or run with
PYTHONPATH=. pytest -v
```

Tests cover:
- Health check endpoint
- GET /search (with and without query)
- POST /search
- PUT /search/{video_id}
- DELETE /search/{video_id}

### Next Steps (Future Integration)
                                    
