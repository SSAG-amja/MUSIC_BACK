from fastapi import APIRouter
from app.api.v1.endpoints import user, login, user_data, loc_wtr

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(user_data.router, prefix="/user_data", tags=["user_data"])

#260202 김호영
#위치 및 날씨 조회 라우터 추가
api_router.include_router(loc_wtr.router, prefix="/loc_wtr", tags=["loc_wtr"])