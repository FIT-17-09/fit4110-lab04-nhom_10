# API Contract - A4 Product A AI Vision Service

## 1. Thong Tin Chung

| Muc | Gia tri |
|---|---|
| Product | Product A |
| Nhom | A4 |
| Service | AI Vision Service |
| Vai tro | Phan tich hinh anh/frame tu Camera Stream |
| Base URL local | `http://localhost:8000` |
| Base URL Docker Compose | `http://ai-vision:8000` |
| OpenAPI file | `contracts/ai-vision.openapi.yaml` |
| Auth | Bearer Token |

## 2. Service Lien Quan

| Provider | Consumer | Y nghia |
|---|---|---|
| A2 Camera Stream | A4 AI Vision | Camera Stream gui frame/anh de AI Vision phan tich |
| A4 AI Vision | A6 Core Business | AI Vision cung cap ket qua phat hien de Core ra quyet dinh/canh bao |
| A4 AI Vision | A5 Analytics | AI Vision cung cap detection log de Analytics thong ke |

## 3. Authentication

Tat ca endpoint nghiep vu can header:

```http
Authorization: Bearer local-dev-token
```

Endpoint `/health` khong can auth.

## 4. Endpoint Cho A2 Goi Sang A4

### POST `/vision/analyze`

Camera Stream gui anh/frame sang AI Vision de phan tich.

### Request Headers

```http
Content-Type: application/json
Authorization: Bearer local-dev-token
```

### Request Body

```json
{
  "camera_id": "cam-gate-01",
  "image_url": "http://example.com/frame.jpg",
  "timestamp": "2026-05-02T09:10:00+07:00",
  "zone": "main_gate",
  "motion_detected": true
}
```

### Request Field

| Field | Type | Required | Mo ta |
|---|---|---:|---|
| `camera_id` | string | Yes | Ma camera gui frame |
| `image_url` | string, URL | Yes | URL anh/frame can phan tich |
| `timestamp` | string, date-time | Yes | Thoi diem frame duoc ghi nhan |
| `zone` | string | No | Khu vuc camera, vi du `main_gate`, `restricted_lab` |
| `motion_detected` | boolean | No | Co phat hien chuyen dong hay khong |

### Response `201 Created`

```json
{
  "analysis_id": "VIS-20260603-0001",
  "camera_id": "cam-gate-01",
  "detected": true,
  "object": "person",
  "confidence": 0.91,
  "risk_level": "medium",
  "detections": [
    {
      "object": "person",
      "confidence": 0.91,
      "bbox": [120, 48, 340, 420]
    }
  ],
  "core_event_url": "http://core-business:8000/events/vision",
  "analytics_event_url": "http://analytics:8000/events/vision",
  "created_at": "2026-06-03T03:00:00+00:00"
}
```

### Response Field

| Field | Type | Mo ta |
|---|---|---|
| `analysis_id` | string | Ma ket qua phan tich, format `VIS-YYYYMMDD-0001` |
| `camera_id` | string | Camera da gui frame |
| `detected` | boolean | Co phat hien doi tuong hay khong |
| `object` | string | Doi tuong chinh duoc phat hien |
| `confidence` | number | Do tin cay, tu `0` den `1` |
| `risk_level` | string | Muc rui ro: `low`, `medium`, `high` |
| `detections` | array | Danh sach detection chi tiet |
| `core_event_url` | string | URL goi y de gui ket qua sang Core Business |
| `analytics_event_url` | string | URL goi y de gui log sang Analytics |
| `created_at` | string | Thoi diem tao ket qua |

### Enum

```text
object = person | stranger | vehicle | bag | none
risk_level = low | medium | high
```

## 5. Endpoint Cho A5 Lay Detection Log

### GET `/vision/results/latest`

Analytics lay danh sach ket qua phan tich moi nhat.

### Query Parameters

| Parameter | Type | Required | Mo ta |
|---|---|---:|---|
| `camera_id` | string | No | Loc theo camera |
| `limit` | integer | No | So ket qua tra ve, tu `1` den `100`, mac dinh `10` |

### Example Request

```http
GET /vision/results/latest?camera_id=cam-gate-01&limit=5
Authorization: Bearer local-dev-token
```

### Response `200 OK`

```json
{
  "items": [
    {
      "analysis_id": "VIS-20260603-0001",
      "camera_id": "cam-gate-01",
      "detected": true,
      "object": "person",
      "confidence": 0.91,
      "risk_level": "medium",
      "detections": [
        {
          "object": "person",
          "confidence": 0.91,
          "bbox": [120, 48, 340, 420]
        }
      ],
      "core_event_url": "http://core-business:8000/events/vision",
      "analytics_event_url": "http://analytics:8000/events/vision",
      "created_at": "2026-06-03T03:00:00+00:00"
    }
  ]
}
```

## 6. Endpoint Lay Mot Ket Qua Cu The

### GET `/vision/results/{analysis_id}`

Lay chi tiet mot ket qua phan tich.

### Example Request

```http
GET /vision/results/VIS-20260603-0001
Authorization: Bearer local-dev-token
```

### Response `200 OK`

Tra ve object giong response cua `POST /vision/analyze`.

## 7. Endpoint Health Check

### GET `/health`

Dung de kiem tra service da san sang hay chua.

### Response `200 OK`

```json
{
  "status": "ok",
  "service": "ai-vision",
  "version": "0.4.0"
}
```

## 8. Error Model

Tat ca loi tra ve theo dang `ProblemDetails`.

### `401 Unauthorized`

```json
{
  "type": "https://smart-campus.local/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Missing Authorization header",
  "instance": "/vision/analyze"
}
```

### `422 Validation Error`

```json
{
  "type": "https://smart-campus.local/problems/validation-error",
  "title": "Validation error",
  "status": 422,
  "detail": "body.image_url: Input should be a valid URL",
  "instance": "/vision/analyze"
}
```

### `404 Not Found`

```json
{
  "type": "https://smart-campus.local/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "Vision analysis VIS-20260603-9999 does not exist",
  "instance": "/vision/results/VIS-20260603-9999"
}
```

## 9. Mapping Ket Qua Cho Core Business A6

A6 co the tao alert khi:

| Dieu kien | Goi y xu ly |
|---|---|
| `object = stranger` va `risk_level = high` | Tao alert muc cao |
| `risk_level = medium` | Ghi nhan event, co the can review |
| `detected = false` va `risk_level = low` | Khong can tao alert |

Payload goi y A4 gui sang A6:

```json
{
  "source_service": "ai-vision",
  "analysis_id": "VIS-20260603-0001",
  "camera_id": "cam-restricted-01",
  "detected": true,
  "object": "stranger",
  "confidence": 0.94,
  "risk_level": "high",
  "timestamp": "2026-05-02T22:10:00+07:00"
}
```

## 10. Mapping Log Cho Analytics A5

A5 co the thong ke theo cac field:

| Metric | Field goi y |
|---|---|
| So lan phat hien | `detected = true` |
| So lan high risk | `risk_level = high` |
| Thong ke theo camera | `camera_id` |
| Thong ke theo loai doi tuong | `object` |
| Do tin cay trung binh | `confidence` |
| Timeline detection | `created_at` |

## 11. Curl Mau

```bash
curl -X POST http://localhost:8000/vision/analyze \
  -H "Authorization: Bearer local-dev-token" \
  -H "Content-Type: application/json" \
  -d '{
    "camera_id": "cam-restricted-01",
    "image_url": "http://example.com/unknown-person.jpg",
    "timestamp": "2026-05-02T22:10:00+07:00",
    "zone": "restricted_lab",
    "motion_detected": true
  }'
```
