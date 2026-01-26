from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

# 260116 김광원
# 회원가입 및 사용자 정보 resopnse

# 공통 속성 (Base)
class UserBase(BaseModel):
    email: EmailStr
    username: str
    gender: str | None = None  # "Male", "Female"
    birth: date | None = None  # YYYY-MM-DD 형식

# 회원가입 시 받을 데이터 (비밀번호 포함)
class UserCreate(UserBase):
    password: str = Field(..., min_length=4, max_length=72) 

# 클라이언트에게 응답할 데이터 (비밀번호 제외, ID 포함)
class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True  # ORM 객체를 Pydantic 모델로 변환 허용 (구 orm_mode)

        