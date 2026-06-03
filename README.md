# FIT4110 Lab 04 - A4 Product A AI Vision

## Service

**A4 Product A AI Vision** builds an AI image analysis service for the Smart Campus Operations Platform.

The service receives image frames from Camera Stream, runs deterministic mock AI inference, and returns detection results for Core Business and Analytics.

## Technology

- Python 3.11
- FastAPI
- Pydantic
- Docker
- Postman/Newman
- OpenAPI 3.1

## Main Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/vision/analyze` | Analyze one image frame |
| `GET` | `/vision/results/latest` | Get latest AI Vision results |
| `GET` | `/vision/results/{analysis_id}` | Get one analysis result |

## Upstream And Downstream

- Upstream: Camera Stream Service sends frames to AI Vision.
- Downstream: Core Business consumes risk results.
- Downstream: Analytics consumes detection metrics.

## Run Local

```bash
pip install -r requirements.txt
uvicorn iot_app.main:app --app-dir src --host 0.0.0.0 --port 8000
```

## Run With Docker

```bash
docker build -t fit4110/ai-vision:lab04 .
docker run --rm --name fit4110-ai-vision-lab04 -p 8000:8000 --env-file .env.example fit4110/ai-vision:lab04
```

## Run With Docker Compose

```bash
docker compose up --build
```

## Run Tests

```bash
npm install
npm run lint:openapi
npm run test:local
```

Newman reports are generated in:

```text
reports/newman-lab04-local.html
reports/newman-lab04-local.xml
```

## Main Artifacts

- `contracts/ai-vision.openapi.yaml`
- `service_boundary.md`
- `endpoint_catalog.md`
- `postman/collections/FIT4110_lab04_ai_vision.postman_collection.json`
- `Dockerfile`
- `.dockerignore`
- `.env.example`
- `docker-compose.yml`
- `RUN_LOCAL.md`
- `reports/docker-evidence.md`
