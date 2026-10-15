from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.schemas.field import FieldResponse,FieldCreate
from app.services.user_service import UserService
from app.services.field_service import FieldService
from fastapi import HTTPException
from app.schemas.alert import AlertResponse
from app.services.alert_service import AlertService
from app.core.security import get_current_user_id


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#must be public so someone can create account without having the jwt token,it is given later
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.create_user(user_data)

#for jwt check
@router.get("/me", response_model=UserResponse)
def get_current_user(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    
    service = UserService(db)

    user = service.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user

@router.get("/me/fields", response_model=list[FieldResponse])
def get_current_user_fields(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    service = FieldService(db)

    return service.get_user_fields(user_id)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    if user_id != current_user_id:
        raise HTTPException(status_code=404, detail="User not found")

    service = UserService(db)
    user = service.get_user(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    if user_id != current_user_id:
        raise HTTPException(status_code=404, detail="User not found")

    service = UserService(db)
    user = service.update_user(user_id, user_data)
    # Convert missing user (None) into an HTTP 404 response
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user



@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    if user_id != current_user_id:
        raise HTTPException(status_code=404, detail="User not found")

    service = UserService(db)
    deleted = service.delete_user(user_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
        
   
# These endpoints are nested under a user (/users/{user_id}/...)
# because the user is the parent resource of the field.     

@router.get("/{user_id}/fields", response_model=list[FieldResponse])
def get_user_fields(
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    if user_id != current_user_id:
        raise HTTPException(status_code=404, detail="User not found")

    user_service = UserService(db)
    user = user_service.get_user(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    field_service = FieldService(db)
    return field_service.get_user_fields(user_id)


# user_id is taken from the path, while field_data is received in the request body.
@router.post(
    "/me/fields",
    response_model=FieldResponse,
    status_code=201
)
def create_current_user_field(
    field_data: FieldCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)

    user = user_service.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    field_service = FieldService(db)

    return field_service.create_field(user_id, field_data)

#to be done wtih auth when we deal with alerts
@router.get(
    "/{user_id}/alerts",
    response_model=list[AlertResponse]
)
def get_user_alerts(
    user_id: int,
    db: Session = Depends(get_db)
) -> list[AlertResponse]:

    user_service = UserService(db)
    alert_service = AlertService(db)

    user = user_service.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return alert_service.get_user_alerts(user_id)

