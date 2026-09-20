from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService
from fastapi import HTTPException

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.create_user(user_data)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    user= service.get_user(user_id)
    # Convert missing user (None) into an HTTP 404 response
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    user = service.update_user(user_id, user_data)

    # Convert missing user (None) into an HTTP 404 response
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    deleted = service.delete_user(user_id)

    # Convert missing user into an HTTP 404 response
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )