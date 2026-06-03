# RUN_LOCAL.md - A4 Product A AI Vision

## 1. Install test tools

```bash
npm install
```

## 2. Run without Docker

```bash
pip install -r requirements.txt
uvicorn iot_app.main:app --app-dir src --host 0.0.0.0 --port 8000
```

Check:

```bash
curl http://localhost:8000/health
```

## 3. Build Docker image

```bash
docker build -t fit4110/ai-vision:lab04 .
```

## 4. Run Docker container

```bash
docker run --rm --name fit4110-ai-vision-lab04 -p 8000:8000 --env-file .env.example fit4110/ai-vision:lab04
```

## 5. Run Newman tests

```bash
npm run test:local
```

Reports:

```text
reports/newman-lab04-local.html
reports/newman-lab04-local.xml
```

## 6. Docker Compose

```bash
docker compose up --build
```

## 7. Registry image

```bash
docker pull vietduck53vb2/fit4110-lab04-ai-vision:v0.1.0-a4-ai-vision
docker run --rm -p 8000:8000 vietduck53vb2/fit4110-lab04-ai-vision:v0.1.0-a4-ai-vision
```
