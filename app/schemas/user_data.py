from pydantic import BaseModel

# 260130 박현식
# 선호 아티스트 및 장르 정보 response

# --- Artist Schemas ---
# 선호 아티스트 공통 속성
class ArtistBase(BaseModel):
    spotify_artist_id: str
    artist_name: str

# 생성 시 받을 데이터
class ArtistCreate(ArtistBase):
    pass

# 응답할 데이터
class ArtistResponse(ArtistBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# --- Genre Schemas ---
# 선호 장르 공통 속성
class GenreBase(BaseModel):
    genre_code: str
    genre_name: str

# 생성 시 받을 데이터
class GenreCreate(GenreBase):
    pass

# 응답할 데이터
class GenreResponse(GenreBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True