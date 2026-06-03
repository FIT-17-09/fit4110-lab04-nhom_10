# Service Boundary - A4 Product A AI Vision

## Role

AI Vision analyzes image frames in the Smart Campus Operations Platform. It receives frames from Camera Stream, runs mock AI inference, and produces detection results for Core Business and Analytics.

## Inputs

- `POST /vision/analyze` from Camera Stream.
- Required fields: `camera_id`, `image_url`, `timestamp`.
- Optional fields: `zone`, `motion_detected`.

## Outputs

- Detection result with `detected`, `object`, `confidence`, and `risk_level`.
- Stored analysis history through `/vision/results/latest` and `/vision/results/{analysis_id}`.
- Integration URLs showing where results should be forwarded:
  - `CORE_SERVICE_URL/events/vision`
  - `ANALYTICS_SERVICE_URL/events/vision`

## Upstream

- Camera Stream Service calls AI Vision when a frame needs analysis.

## Downstream

- Core Business Service receives AI results to decide whether an alert is needed.
- Analytics Service receives AI events for reports and metrics.

## Service Boundary Table

| Direction | Service | Purpose |
|---|---|---|
| Incoming | Camera Stream | Sends image/frame URL for analysis |
| Outgoing | Core Business | Provides risk result for policy decision |
| Outgoing | Analytics | Provides detection metrics |

## Notes

This lab uses deterministic mock AI instead of a heavy YOLO model so the Docker image can run reliably on classroom machines. The mock rules are documented and tested: unknown/restricted inputs produce high risk, normal person frames produce medium risk, and no-motion frames produce low risk.
