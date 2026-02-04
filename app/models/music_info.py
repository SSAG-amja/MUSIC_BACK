from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base  # db/base.py에 정의된 Base 객체를 임포트

# 260203 김호영
# musics 테이블 정의
class Music(Base):
    __tablename__ = "musics"

    music_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    spotify_id = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    artist = Column(String(100), nullable=False)
    album_cover = Column(Text)

    # Relationships: 이 음악이 포함된 플레이리스트 트랙들과 다이어리
    playlist_tracks = relationship("PlaylistTrack", back_populates="music")
    diaries = relationship("MusicDiary", back_populates="music")

# 260203 김호영
# playlists 테이블 정의
class Playlist(Base):
    __tablename__ = "playlists"

    playlist_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # User 모델의 PK 참조
    original_playlist_id = Column(BigInteger, ForeignKey("playlists.playlist_id"), nullable=True) # 자기 참조 (저작권용)
    title = Column(String(100), default="현재 재생중인 플레이리스트")
    
    # 외부 연동 데이터 (날씨, 위치 등)
    weather = Column(String(50))
    location = Column(String(100))
    mood = Column(String(50))
    situation = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="playlists") # User 모델 쪽에 playlists relationship 필요
    tracks = relationship("PlaylistTrack", back_populates="playlist", cascade="all, delete-orphan")

# 260203 김호영
# playlists_tracks 테이블 정의
class PlaylistTrack(Base):
    __tablename__ = "playlists_tracks"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    playlist_id = Column(BigInteger, ForeignKey("playlists.playlist_id"), nullable=False)
    music_id = Column(BigInteger, ForeignKey("musics.music_id"), nullable=False)
    order_index = Column(Integer, nullable=False)

    # Relationships
    playlist = relationship("Playlist", back_populates="tracks")
    music = relationship("Music", back_populates="playlist_tracks")

# 260203 김호영
# music_diaries 테이블 정의
# music_diaries도 musics를 참조함으로 그냥 하나로 묶었음
class MusicDiary(Base):
    __tablename__ = "music_diaries"

    diary_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    music_id = Column(BigInteger, ForeignKey("musics.music_id"), nullable=False)
    content = Column(Text)
    
    # 외부 연동 데이터
    weather = Column(String(50))
    location = Column(String(100))
    mood = Column(String(50))
    situation = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="diaries")
    music = relationship("Music", back_populates="diaries")