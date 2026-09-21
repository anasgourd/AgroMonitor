from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.field import FieldResponse,FieldCreate
from app.services.field_service import FieldService
from fastapi import HTTPException


user_field_router = APIRouter(
    prefix="/users",
    tags=["Fields"]
)

# field_router = APIRouter(
#     prefix="/fields",
#     tags=["Fields"]
# )

