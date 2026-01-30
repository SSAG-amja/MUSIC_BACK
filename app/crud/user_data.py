from sqlalchemy.orm import Session
from app.models.user_data import UserPreferredArtist, UserPreferredGenre
from app.schemas.user_data import ArtistCreate, GenreCreate

# 260130 박현식
# 아티스트 선호 정보 저장
def create_artist_preference(db: Session, artist: ArtistCreate, user_id: int):
    db_obj = UserPreferredArtist(
        user_id=user_id,
        spotify_artist_id=artist.spotify_artist_id,
        artist_name=artist.artist_name
    )
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)  # DB에서 생성된 ID 등 데이터를 갱신
    return db_obj

# 260130 박현식
# 장르 선호 정보 저장
def create_genre_preference(db: Session, genre: GenreCreate, user_id: int):
    db_obj = UserPreferredGenre(
        user_id=user_id,
        genre_code=genre.genre_code,
        genre_name=genre.genre_name
    )
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)  # DB에서 생성된 ID 등 데이터를 갱신
    return db_obj