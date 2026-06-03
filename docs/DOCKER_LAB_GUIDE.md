# Docker Lab Guide - A4 AI Vision

## Build

```bash
docker build -t fit4110/ai-vision:lab04 .
```

## Run

```bash
docker run --rm --name fit4110-ai-vision-lab04 -p 8000:8000 --env-file .env.example fit4110/ai-vision:lab04
```

## Health

```bash
curl http://localhost:8000/health
```

Expected:

```json
{"status":"ok","service":"ai-vision","version":"0.4.0"}
```

## Test

```bash
npm run test:local
```

## Inspect

```bash
docker inspect fit4110-ai-vision-lab04
```
