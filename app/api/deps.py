from app.db.session import SessionLocal
from typing import Generator

# 260103 김광원
# 의존성, 세션 관리 함수마다 DB 세션 공유 (모든 DB작업의 시작점)
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()