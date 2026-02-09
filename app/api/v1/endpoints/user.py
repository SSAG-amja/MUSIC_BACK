from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.core.security import verify_password
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.models.user import User as models_user

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

# 260204 김광원
# 회원정보 수정
@router.get("/me")
def get_user_profile(
    current_user: UserResponse = Depends(get_current_user)
):
    return {
        "email" : current_user.email,
        "username" : current_user.username,
        "gender" : current_user.gender,
        "birth" : current_user.birth,
        "is_newer" : current_user.is_newer,
    }

@router.put("/me")
def update_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: models_user = Depends(get_current_user)
    ):
    updated_user = crud_user.update_user(db=db, user=current_user, user_in=user_update)

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비밀번호가 일치하지 않습니다."
        )

    return {"message": "회원정보가 수정되었습니다.", "user": current_user.username}