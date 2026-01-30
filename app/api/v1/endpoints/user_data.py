from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any

from app.api.deps import get_db, get_current_user
from app.crud import user_data as crud_user_data
from app.schemas.user_data import ArtistCreate, ArtistResponse, GenreCreate, GenreResponse
from app.models.user import User

router = APIRouter()

# 260130 박현식
# 선호 아티스트 등록
@router.post("/artists", response_model=ArtistResponse)
def add_preferred_artist(
    artist_in: ArtistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 로그인된 유저 정보 자동 추출
) -> Any:
    # current_user.id를 사용하여 안전하게 저장
    return crud_user_data.create_artist_preference(db=db, artist=artist_in, user_id=current_user.id)

# 260130 박현식
# 선호 장르 등록
@router.post("/genres", response_model=GenreResponse)
def add_preferred_genre(
    genre_in: GenreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    return crud_user_data.create_genre_preference(db=db, genre=genre_in, user_id=current_user.id)