# Integration Notes - A4 Product A AI Vision

## Producer

Camera Stream Service sends frames to:

```text
POST http://ai-vision:8000/vision/analyze
```

## Consumers

AI Vision exposes results for:

- Core Business: risk decision and alert creation.
- Analytics: detection count, high-risk count, per-camera metrics.

## Runtime Environment

```text
CORE_SERVICE_URL=http://core-business:8000
ANALYTICS_SERVICE_URL=http://analytics:8000
AUTH_TOKEN=local-dev-token
```

## End-to-End Demo Flow

1. Camera Stream detects motion at `cam-restricted-01`.
2. Camera Stream calls AI Vision `/vision/analyze` with an `unknown-person.jpg` frame URL.
3. AI Vision returns `object=stranger`, `confidence=0.94`, `risk_level=high`.
4. Core Business can create an alert from that result.
5. Analytics can count the high-risk detection.
