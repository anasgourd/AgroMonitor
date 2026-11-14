from fastapi import APIRouter
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

router = APIRouter()


@router.get("/metrics")
def get_metrics():
    
    if os.getenv("METRICS_ENABLED", "false").lower() != "true":
        raise HTTPException(status_code=404, detail="Not Found")
    
    # Expose the current Prometheus metrics in the format
    # expected by Prometheus.
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )