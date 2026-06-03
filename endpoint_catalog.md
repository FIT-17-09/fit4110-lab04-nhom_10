# Endpoint Catalog - A4 Product A AI Vision

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `GET` | `/health` | No | Docker and integration health check |
| `POST` | `/vision/analyze` | Bearer token | Analyze one image frame |
| `GET` | `/vision/results/latest` | Bearer token | Return latest analysis results |
| `GET` | `/vision/results/{analysis_id}` | Bearer token | Return one analysis result |

## Main Request

```json
{
  "camera_id": "cam-gate-01",
  "image_url": "http://example.com/frame.jpg",
  "timestamp": "2026-05-02T09:10:00+07:00",
  "zone": "main_gate",
  "motion_detected": true
}
```

## Main Response

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
