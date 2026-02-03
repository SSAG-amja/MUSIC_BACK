from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from typing import Optional

# [중요] 분리된 models와 schemas 폴더에서 music_info.py를 각각 불러옵니다.
from app.models import music_info as models
from app.schemas import music_info as schemas

# 260203 김호영
# Music CRUD 함수 구현
# ==========================================
# 1. Music (음악 캐싱 로직)
# ==========================================
def get_or_create_music(db: Session, music_in: schemas.MusicCreate):
    """
    DB에 해당 스포티파이 ID의 노래가 있는지 확인하고,
    있으면 반환, 없으면 새로 저장(캐싱)하여 중복 저장을 방지합니다.
    """
    existing_music = db.query(models.Music).filter(
        models.Music.spotify_id == music_in.spotify_id
    ).first()

    if existing_music:
        return existing_music

    new_music = models.Music(**music_in.model_dump())
    db.add(new_music)
    db.commit()
    db.refresh(new_music)
    return new_music

# 260203 김호영
# Playlist CRUD 함수 구현
# ==========================================
# 2. Playlist (플레이리스트 CRUD)
# ==========================================
def create_playlist(db: Session, playlist_in: schemas.PlaylistCreate, user_id: str):
    """
    플레이리스트를 생성합니다. (수록곡 포함 여부에 따라 유동적으로 동작)
    """
    playlist_data = playlist_in.model_dump(exclude={"tracks"})
    new_playlist = models.Playlist(**playlist_data, user_id=user_id)
    
    db.add(new_playlist)
    db.flush() # ID를 먼저 발급받기 위해 flush (commit은 나중에)

    # tracks 데이터가 함께 들어왔다면 한 번에 묶어서 저장
    if playlist_in.tracks:
        for track_in in playlist_in.tracks:
            new_track = models.PlaylistTrack(
                playlist_id=new_playlist.playlist_id,
                music_id=track_in.music_id,
                order_index=track_in.order_index
            )
            db.add(new_track)
    
    db.commit()
    db.refresh(new_playlist)
    return new_playlist

def get_playlists(
    db: Session, 
    user_id: Optional[str] = None, 
    is_public: Optional[bool] = None, 
    weather: Optional[str] = None,
    mood: Optional[str] = None
):
    """
    플레이리스트 목록을 조회합니다. 조건에 따른 동적 필터링을 지원합니다.
    """
    query = db.query(models.Playlist)\
        .options(joinedload(models.Playlist.tracks).joinedload(models.PlaylistTrack.music))
    
    # 전달된 조건이 있을 때만 필터링 적용 (다이내믹 쿼리)
    if user_id:
        query = query.filter(models.Playlist.user_id == user_id)
    if is_public is not None:
        query = query.filter(models.Playlist.is_public == is_public)
    if weather:
        query = query.filter(models.Playlist.weather == weather)
    if mood:
        query = query.filter(models.Playlist.mood == mood)
        
    return query.order_by(models.Playlist.created_at.desc()).all()

def get_playlist_with_details(db: Session, playlist_id: int):
    """
    플레이리스트 1개와 그 수록곡, 음악 원본 정보까지 한 번에 조회합니다.
    """
    return db.query(models.Playlist)\
        .options(joinedload(models.Playlist.tracks).joinedload(models.PlaylistTrack.music))\
        .filter(models.Playlist.playlist_id == playlist_id)\
        .first()

def update_playlist_tracks(db: Session, playlist_id: int, tracks_in: schemas.PlaylistTracksUpdate, user_id: str):
    """
    [핵심] 플레이리스트 수록곡의 순서나 목록을 수정합니다.
    기존 트랙을 모두 삭제하고, 새로운 트랙을 다시 삽입하는 방식입니다.
    """
    playlist = db.query(models.Playlist).filter(models.Playlist.playlist_id == playlist_id).first()
    
    # 존재 여부 및 소유권 확인
    if not playlist or playlist.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="수정 권한이 없습니다.")

    # 1. 기존 트랙 모두 삭제
    db.query(models.PlaylistTrack).filter(models.PlaylistTrack.playlist_id == playlist_id).delete()
    
    # 2. 새로운 트랙 순서대로 삽입
    for track in tracks_in.tracks:
        new_track = models.PlaylistTrack(
            playlist_id=playlist_id,
            music_id=track.music_id,
            order_index=track.order_index
        )
        db.add(new_track)
        
    db.commit()
    return get_playlist_with_details(db, playlist_id)

def delete_playlist(db: Session, playlist_id: int, user_id: str):
    """
    플레이리스트를 삭제합니다. (수록곡 매핑은 삭제되나, 음악 캐시는 유지됨)
    """
    playlist = db.query(models.Playlist).filter(models.Playlist.playlist_id == playlist_id).first()
    
    if not playlist:
        return False
    if playlist.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="삭제 권한이 없습니다.")

    db.delete(playlist)
    db.commit()
    return True

# 260203 김호영
# Music Diary CRUD 함수 구현
# ==========================================
# 3. Music Diary (다이어리 CRUD)
# ==========================================
def create_music_diary(db: Session, diary_in: schemas.MusicDiaryCreate, user_id: str):
    diary_data = diary_in.model_dump()
    new_diary = models.MusicDiary(**diary_data, user_id=user_id)
    
    db.add(new_diary)
    db.commit()
    db.refresh(new_diary)
    return new_diary

def get_diary_with_music(db: Session, diary_id: int):
    return db.query(models.MusicDiary)\
        .options(joinedload(models.MusicDiary.music))\
        .filter(models.MusicDiary.diary_id == diary_id)\
        .first()