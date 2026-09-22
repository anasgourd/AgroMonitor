from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.field import FieldResponse, FieldUpdate
from app.services.field_service import FieldService
from fastapi import HTTPException


router = APIRouter(
    prefix="/fields",
    tags=["Fields"]
)


@router.get("/{field_id}", response_model=FieldResponse)
def get_field(
    field_id: int,
    db: Session = Depends(get_db)
):
    service = FieldService(db)

    field = service.get_field(field_id)

    if field is None:
        raise HTTPException(
            status_code=404,
            detail="Field not found"
        )

    return field

@router.put("/{field_id}", response_model=FieldResponse)
def update_field(
    field_id: int,
    field_data: FieldUpdate,
    db: Session = Depends(get_db)
):
    service = FieldService(db)

    field = service.update_field(field_id, field_data)

    if field is None:
        raise HTTPException(
            status_code=404,
            detail="Field not found"
        )

    return field

@router.delete("/{field_id}", status_code=204)
def delete_field(
    field_id: int,
    db: Session = Depends(get_db)
):
    service = FieldService(db)

    deleted = service.delete_field(field_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Field not found"
        )