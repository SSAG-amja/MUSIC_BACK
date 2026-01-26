from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

# 260116 김광원
# 이메일 중복 체크
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# 260116 김광원
# username 중복 체크
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# 260116 김광원
# 유저 생성
def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    
    db_obj = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        gender=user.gender,
        birth=user.birth,
        is_active=True
    )
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj) # DB에서 생성된 ID 등 데이터를 갱신
    return db_obj 