from sqlalchemy import Column, Integer, String, Boolean, Date
from app.db.base import Base

# 260116 김광원
# users 테이블 정의
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    username = Column(String, index=True, nullable=False)
    gender = Column(String, nullable=False)            
    birth = Column(Date, nullable=False)            
    is_active = Column(Boolean, default=True) # soft delete(현업에서 자주 사용)