from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

# 260103 김광원
# User 모델 정의
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False) # JWT 발급 시 검증할 비밀번호(해시됨)
    is_active = Column(Boolean, default=True)