from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from app.api.deps import get_db, get_current_user
from app.crud import user_data as crud_user_data
from app.crud import user as crud_user
from app.schemas.user_data import ArtistCreate, ArtistResponse, GenreCreate, GenreResponse, NewerPreferencesCreate, NewerPreferencesResponse
from app.models.user import User


router = APIRouter()

# 260204 김광원
# 함수로직 분리 (Refeactor)
def process_add_artist(
        db: Session, 
        user_id: int, 
        artist_in: ArtistCreate
) -> ArtistResponse :
    return crud_user_data.create_artist_preference(db=db, artist=artist_in, user_id=user_id)

def process_add_genre(
        db: Session, 
        user_id: int, 
        genre_in: GenreCreate
) -> GenreResponse :
    return crud_user_data.create_genre_preference(db=db, genre=genre_in, user_id=user_id)

# 260130 박현식
# 선호 아티스트 등록
@router.post("/artists", response_model=ArtistResponse)
def add_preferred_artist(
    artist_in: ArtistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 로그인된 유저 정보 자동 추출
) -> Any:
    # current_user.id를 사용하여 안전하게 저장
    return process_add_artist(db=db, user_id=current_user.id, artist_in=artist_in)

# 260130 박현식
# 선호 장르 등록
@router.post("/genres", response_model=GenreResponse)
def add_preferred_genre(
    genre_in: GenreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    return process_add_genre(db=db, user_id=current_user.id, genre_in=genre_in)

# 260204 김광원
# Newer 한번에 처리하도록
@router.post("/batch", response_model=NewerPreferencesResponse)
def add_artist_and_genre(
        preferences_in: NewerPreferencesCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> Any:
    try: 
        artist_res = process_add_artist(db=db, user_id=current_user.id, artist_in=preferences_in.artist)
        genre_res = process_add_genre(db=db, user_id=current_user.id, genre_in=preferences_in.genre)

        crud_user.update_is_newer(db=db, user=current_user)
        return NewerPreferencesResponse(
            artist=artist_res,
            genre=genre_res
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))