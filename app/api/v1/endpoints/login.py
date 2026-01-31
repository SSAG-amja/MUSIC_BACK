from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from requests import Session

from app.schemas.token import LoginRespose
from app.core.config import TOKEN_EXP_TIME
from app.core import security

from app.api.deps import get_db
from app.crud import user as crud_user

router = APIRouter()

# 260131 김광원
# 로그인(토큰 값 반환 및 신규 유저인지 반환)
@router.post("/", response_model=LoginRespose)
def signin(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends() # Swagger Authorize 활성화
) -> Any:
    user = crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="email, password가 일치하지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = security.create_access_token(
        data={"sub": str(user.id)},
        exp_delta=timedelta(minutes=int(TOKEN_EXP_TIME)),
    )

    is_newer = crud_user.check_newer(db, email=user.email)

    return{
        "access_token": access_token,
        "token_type" : "bearer",
        "is_newer": is_newer
    }