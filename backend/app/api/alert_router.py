from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.alert import AlertResponse
from app.services.alert_service import AlertService


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get(
    "/{alert_id}",
    response_model=AlertResponse
)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db)
) -> AlertResponse:
    service = AlertService(db)

    alert = service.get_alert(alert_id)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert