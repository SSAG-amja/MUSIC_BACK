from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

# 260103 김광원
# DB 세션관리
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
