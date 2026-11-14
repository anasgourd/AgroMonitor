from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService
from fastapi import Request
from app.core.rate_limit import limiter

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login(
    request: Request,
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    service = AuthService(db)

    token = service.login(
        login_data.username,
        login_data.password
    )

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
    
