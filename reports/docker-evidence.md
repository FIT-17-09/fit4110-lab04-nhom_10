# Docker Evidence - Lab 04 A4 AI Vision

## Team

- Team name: nhom_10
- Topic: A4 Product A AI Vision
- Service: ai-vision
- Local image tag: `fit4110/ai-vision:lab04`
- Registry image tag: `vietduck53vb2/fit4110-lab04-ai-vision:v0.1.0-a4-ai-vision`
- Registry digest: `sha256:42ac7e1c148a28f1e2257d4db485e6ede113701d094a9faf83aaaa350b3473c4`

## 1. Build Evidence

Command:

```bash
docker build -t fit4110/ai-vision:lab04 .
```

## 2. Run Evidence

Command:

```bash
docker run -d --rm --name fit4110-ai-vision-lab04 -p 8000:8000 --env-file .env.example fit4110/ai-vision:lab04
```

Expected container health:

```text
running healthy
```

## 3. Healthcheck Evidence

Command:

```bash
curl http://localhost:8000/health
```

Expected result:

```json
{"status":"ok","service":"ai-vision","version":"0.4.0"}
```

## 4. Newman Evidence

Command:

```bash
npm run test:local
```

Expected result:

```text
requests: 11 executed, 0 failed
assertions: all passed
```

Report paths:

```text
reports/newman-lab04-local.html
reports/newman-lab04-local.xml
```

## 5. Integration Evidence

- Camera Stream calls `POST /vision/analyze`.
- AI Vision returns `risk_level` for Core Business.
- AI Vision exposes latest results for Analytics.
- Integration URLs are configured by `CORE_SERVICE_URL` and `ANALYTICS_SERVICE_URL`.

## 6. Notes

- The service uses deterministic mock AI instead of YOLO to keep Docker builds lightweight.
- Dockerfile uses `python:3.11-slim`, non-root user `appuser`, and container `HEALTHCHECK`.
- Error responses use `application/problem+json` ProblemDetails for auth and validation cases.
