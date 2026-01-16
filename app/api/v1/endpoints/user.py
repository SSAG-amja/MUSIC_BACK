from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

# 260116 김광원
# 회원가입
@router.post("/", response_model=UserResponse)
def signup(
    user_in: UserCreate,       
    db: Session = Depends(get_db)
):
    
    # 이메일 중복 체크
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="이미 사용중인 email 입니다",
        )
    
    # username 중복 체크
    user = crud_user.get_user_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="이미 사용중인 username 입니다",
        )
    
    
    # 유저 생성 (CRUD 함수 호출 -> 내부에서 해싱됨)
    user = crud_user.create_user(db=db, user=user_in)
    return user