import os
from datetime import datetime, timezone
from enum import Enum
from http import HTTPStatus
from typing import Dict, List, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, HttpUrl


SERVICE_NAME = os.getenv("SERVICE_NAME", "ai-vision")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "0.4.0")
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "local-dev-token")
CORE_SERVICE_URL = os.getenv("CORE_SERVICE_URL", "http://core-business:8000")
ANALYTICS_SERVICE_URL = os.getenv("ANALYTICS_SERVICE_URL", "http://analytics:8000")


app = FastAPI(
    title="FIT4110 Lab 04 - A4 Product A AI Vision Service",
    version=SERVICE_VERSION,
    description=(
        "Dockerized AI Vision API for Smart Campus image analysis. "
        "The service receives frames from Camera Stream and returns mock AI detections "
        "for Core Business and Analytics integration."
    ),
)


class DetectedObject(str, Enum):
    person = "person"
    stranger = "stranger"
    vehicle = "vehicle"
    bag = "bag"
    none = "none"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ProblemDetails(BaseModel):
    type: str = "about:blank"
    title: str
    status: int = Field(..., ge=400, le=599)
    detail: str
    instance: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class VisionAnalyzeRequest(BaseModel):
    camera_id: str = Field(..., min_length=3, examples=["cam-gate-01"])
    image_url: HttpUrl = Field(..., examples=["http://example.com/frame.jpg"])
    timestamp: str = Field(..., examples=["2026-05-02T09:10:00+07:00"])
    zone: Optional[str] = Field(default="main_gate", examples=["main_gate"])
    motion_detected: bool = Field(default=True, examples=[True])


class Detection(BaseModel):
    object: DetectedObject
    confidence: float = Field(..., ge=0, le=1)
    bbox: List[int] = Field(..., min_length=4, max_length=4)


class VisionAnalysisResult(BaseModel):
    analysis_id: str
    camera_id: str
    detected: bool
    object: DetectedObject
    confidence: float = Field(..., ge=0, le=1)
    risk_level: RiskLevel
    detections: List[Detection]
    core_event_url: str
    analytics_event_url: str
    created_at: str


ANALYSES: List[Dict] = []


def status_title(status_code: int) -> str:
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return "HTTP Error"


def build_problem(
    *,
    status_code: int,
    title: str,
    detail: str,
    instance: Optional[str] = None,
    problem_type: str = "about:blank",
) -> Dict:
    problem = {
        "type": problem_type,
        "title": title,
        "status": status_code,
        "detail": detail,
    }
    if instance:
        problem["instance"] = instance
    return problem


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc.detail, dict):
        problem = exc.detail
    else:
        problem = build_problem(
            status_code=exc.status_code,
            title=status_title(exc.status_code),
            detail=str(exc.detail),
            instance=str(request.url.path),
        )

    problem.setdefault("status", exc.status_code)
    problem.setdefault("title", status_title(exc.status_code))
    problem.setdefault("type", "about:blank")
    problem.setdefault("detail", "Request failed")
    problem.setdefault("instance", str(request.url.path))

    return JSONResponse(
        status_code=exc.status_code,
        content=problem,
        media_type="application/problem+json",
        headers=getattr(exc, "headers", None),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    first_error = exc.errors()[0] if exc.errors() else {}
    location = ".".join(str(item) for item in first_error.get("loc", []))
    message = first_error.get("msg", "Request validation error")
    detail = f"{location}: {message}" if location else message

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=build_problem(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            title="Validation error",
            detail=detail,
            instance=str(request.url.path),
            problem_type="https://smart-campus.local/problems/validation-error",
        ),
        media_type="application/problem+json",
    )


def verify_bearer_token(authorization: Optional[str] = Header(default=None)) -> None:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=build_problem(
                status_code=status.HTTP_401_UNAUTHORIZED,
                title="Unauthorized",
                detail="Missing Authorization header",
                problem_type="https://smart-campus.local/problems/unauthorized",
            ),
        )

    expected = f"Bearer {AUTH_TOKEN}"
    if authorization != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=build_problem(
                status_code=status.HTTP_401_UNAUTHORIZED,
                title="Unauthorized",
                detail="Invalid bearer token",
                problem_type="https://smart-campus.local/problems/unauthorized",
            ),
        )


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def next_analysis_id() -> str:
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"VIS-{today}-{len(ANALYSES) + 1:04d}"


def run_mock_ai(payload: VisionAnalyzeRequest) -> Dict:
    text = f"{payload.camera_id} {payload.image_url} {payload.zone}".lower()

    if not payload.motion_detected:
        detected_object = DetectedObject.none
        confidence = 0.08
    elif "unknown" in text or "stranger" in text or "restricted" in text:
        detected_object = DetectedObject.stranger
        confidence = 0.94
    elif "vehicle" in text:
        detected_object = DetectedObject.vehicle
        confidence = 0.87
    elif "bag" in text:
        detected_object = DetectedObject.bag
        confidence = 0.78
    else:
        detected_object = DetectedObject.person
        confidence = 0.91

    if detected_object == DetectedObject.stranger or confidence >= 0.93:
        risk_level = RiskLevel.high
    elif confidence >= 0.75 and detected_object != DetectedObject.none:
        risk_level = RiskLevel.medium
    else:
        risk_level = RiskLevel.low

    detected = detected_object != DetectedObject.none
    detections = []
    if detected:
        detections.append(
            Detection(
                object=detected_object,
                confidence=confidence,
                bbox=[120, 48, 340, 420],
            ).model_dump()
        )

    return {
        "detected": detected,
        "object": detected_object.value,
        "confidence": confidence,
        "risk_level": risk_level.value,
        "detections": detections,
    }


def health_payload() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=SERVICE_NAME,
        version=SERVICE_VERSION,
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return health_payload()


@app.head("/health", status_code=status.HTTP_200_OK)
def health_head() -> None:
    return None


@app.post(
    "/vision/analyze",
    response_model=VisionAnalysisResult,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_bearer_token)],
    responses={
        401: {"model": ProblemDetails},
        422: {"model": ProblemDetails},
    },
)
def analyze_image(payload: VisionAnalyzeRequest) -> VisionAnalysisResult:
    ai_result = run_mock_ai(payload)
    analysis_id = next_analysis_id()
    created_at = now_iso()

    item = {
        "analysis_id": analysis_id,
        "camera_id": payload.camera_id,
        **ai_result,
        "core_event_url": f"{CORE_SERVICE_URL}/events/vision",
        "analytics_event_url": f"{ANALYTICS_SERVICE_URL}/events/vision",
        "created_at": created_at,
    }
    ANALYSES.append(item)

    return VisionAnalysisResult(**item)


@app.get("/vision/results/latest", dependencies=[Depends(verify_bearer_token)])
def latest_results(
    camera_id: Optional[str] = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
) -> Dict[str, List[Dict]]:
    items = ANALYSES

    if camera_id:
        items = [item for item in items if item["camera_id"] == camera_id]

    return {"items": items[-limit:]}


@app.get("/vision/results/{analysis_id}", dependencies=[Depends(verify_bearer_token)])
def get_result(analysis_id: str) -> Dict:
    for item in ANALYSES:
        if item["analysis_id"] == analysis_id:
            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=build_problem(
            status_code=status.HTTP_404_NOT_FOUND,
            title="Not Found",
            detail=f"Vision analysis {analysis_id} does not exist",
            instance=f"/vision/results/{analysis_id}",
            problem_type="https://smart-campus.local/problems/not-found",
        ),
    )
