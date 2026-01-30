from sqlalchemy import Column, String, Integer, ForeignKey
from app.db.base import Base

# 260130 박현식
# preferred_artists 테이블 정의
class UserPreferredArtist(Base):
    __tablename__ = "user_preferred_artists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    spotify_artist_id = Column(String, nullable=False)
    artist_name = Column(String, nullable=False)


# 260130 박현식
# preferred_genres 테이블 정의
class UserPreferredGenre(Base):
    __tablename__ = "user_preferred_genres"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    genre_code = Column(String, nullable=False)
    genre_name = Column(String, nullable=False)
