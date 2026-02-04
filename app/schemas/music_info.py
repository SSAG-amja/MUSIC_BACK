from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime

# ==========================================
# 1. Music (음악 기본 정보)
# ==========================================
class MusicBase(BaseModel):
    spotify_id: str = Field(..., max_length=100)
    title: str = Field(..., max_length=200)
    artist: str = Field(..., max_length=100)
    album_cover: Optional[str] = None

class MusicCreate(MusicBase):
    pass 

class MusicResponse(MusicBase):
    music_id: int
    
    # ORM 모델(SQLAlchemy)을 Pydantic 객체로 자동 변환 (v2 문법)
    model_config = ConfigDict(from_attributes=True) 


# ==========================================
# 2. Playlist Track (플레이리스트 수록곡)
# ==========================================
class PlaylistTrackBase(BaseModel):
    order_index: int

class PlaylistTrackCreate(PlaylistTrackBase):
    music_id: int

# [추가됨] 기존 플레이리스트에 여러 곡을 나중에 추가할 때 사용
class PlaylistTrackBulkAdd(BaseModel):
    playlist_id: int
    tracks: List[PlaylistTrackCreate]

class PlaylistTrackResponse(PlaylistTrackBase):
    id: int
    music: MusicResponse # 곡의 상세 정보 포함

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 3. Playlist (플레이리스트)
# ==========================================
class PlaylistBase(BaseModel):
    title: str = Field(default="새로운 플레이리스트", max_length=100)
    # 프론트엔드 캐시 정보 (위치, 날씨 등)
    weather: Optional[str] = Field(None, max_length=50) 
    location: Optional[str] = Field(None, max_length=100)
    mood: Optional[str] = Field(None, max_length=50)
    situation: Optional[str] = Field(None, max_length=50)

class PlaylistCreate(PlaylistBase):
    original_playlist_id: Optional[int] = None
    # user_id는 토큰에서 추출하므로 제외됨
    # tracks가 None이면 '껍데기만 생성', 리스트가 있으면 '한 번에 생성'
    tracks: Optional[List[PlaylistTrackCreate]] = None 

class PlaylistResponse(PlaylistBase):
    playlist_id: int
    user_id: str # 응답에는 작성자 정보 포함
    original_playlist_id: Optional[int]
    created_at: datetime
    # 수록곡 및 음악 상세 정보가 포함된 리스트
    tracks: List[PlaylistTrackResponse] 

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 4. Music Diary (음악 다이어리)
# ==========================================
class MusicDiaryBase(BaseModel):
    content: str
    weather: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=100)
    mood: Optional[str] = Field(None, max_length=50)
    situation: Optional[str] = Field(None, max_length=50)

class MusicDiaryCreate(MusicDiaryBase):
    music_id: int # 연결할 음악 ID
    # user_id는 토큰에서 추출하므로 제외됨

class MusicDiaryResponse(MusicDiaryBase):
    diary_id: int
    user_id: str
    created_at: datetime
    music: MusicResponse # 일기 작성 시 선택한 음악 상세 정보 포함

    model_config = ConfigDict(from_attributes=True)