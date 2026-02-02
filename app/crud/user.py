from sqlalchemy.orm import Session
from sqlalchemy import exists
from app.models.user import User
from app.models.user_data import UserPreferredArtist, UserPreferredGenre
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
        is_active=True,
        is_newer=True
    )
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj) # DB에서 생성된 ID 등 데이터를 갱신
    return db_obj 

# 260131 김광원
# 신규 유저인지 확인
def check_newer(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()

    if user:
        return user.is_newer
    return False

# 260131 김광원
# user data table에 데이터 존재하는 경우 is_newer False로 
def update_is_newer(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    
    has_artist = db.query(exists().where(UserPreferredArtist.user_id == user.id)).scalar()
    has_genre = db.query(exists().where(UserPreferredGenre.user_id == user.id)).scalar()

    if has_artist or has_genre:
        user.is_newer = False
        db.commit()
        db.refresh(user)
        return True
    
    return False