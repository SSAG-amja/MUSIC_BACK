from fastapi import APIRouter, HTTPException
import httpx
from app.core import config  #config.py에서 API키 불러오기
from app.schemas.loc_wtr import WeatherResponse 

router = APIRouter()

# 260202 김호영
# 위치 및 날씨 조회 API 작성
@router.get("/getLocWtr", response_model=WeatherResponse)
async def get_location_and_weather(lat: float, lon: float):
    
    # config.py 변수 직접 사용
    KAKAO_KEY = config.KAKAO_REST_API_KEY
    GOOGLE_KEY = config.GOOGLE_MAPS_API_KEY

    # 키가 없으면 에러 (서버 로그용)
    if not KAKAO_KEY or not GOOGLE_KEY:
        print("❌ [ERROR] API Key Missing in config.py")
        raise HTTPException(status_code=500, detail="Server Configuration Error")

    async with httpx.AsyncClient() as client:
        try:
            # -------------------------------------------------
            # [A] 카카오: 좌표 -> 주소
            # -------------------------------------------------
            kakao_res = await client.get(
                "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json",
                headers={"Authorization": f"KakaoAK {KAKAO_KEY}"},
                params={"x": lon, "y": lat} 
            )
            kakao_data = kakao_res.json()
            
            city, district, dong = "위치미상", "", ""
            if kakao_data.get('documents'):
                addr = kakao_data['documents'][0]
                city = addr['region_1depth_name']
                district = addr['region_2depth_name']
                dong = addr['region_3depth_name']

            # -------------------------------------------------
            # [B] 구글: 좌표 -> 날씨
            # -------------------------------------------------
            google_res = await client.get(
                "https://weather.googleapis.com/v1/currentConditions:lookup",
                params={
                    "key": GOOGLE_KEY,
                    "location.latitude": lat,
                    "location.longitude": lon,
                    "unitsSystem": "METRIC",
                    "languageCode": "ko"
                }
            )
            google_data = google_res.json()

            print("================ 구글 날씨 원본 데이터 ================")
            print(google_data) 
            print("======================================================")

            temp = 0
            weather_desc = "정보 없음"
            weather_code = "clear"

            if "currentConditions" in google_data:
                cond = google_data["currentConditions"]
                temp = cond.get("temperature", {}).get("value", 0)
                weather_desc = cond.get("conditionDescription", "")
                weather_code = cond.get("weatherCondition", "clear")

            # 상태 매핑 (음악 추천용)
            status = "Clear"
            code_lower = weather_code.lower()
            if any(x in code_lower for x in ["rain", "drizzle", "shower", "thunder"]):
                status = "Rain"
            elif any(x in code_lower for x in ["snow", "ice", "hail"]):
                status = "Snow"
            elif any(x in code_lower for x in ["cloud", "overcast"]):
                status = "Clouds"
            elif any(x in code_lower for x in ["fog", "mist", "haze"]):
                status = "Atmosphere"

        except Exception as e:
            print(f"❌ API Error: {e}")
            # 에러 발생 시 프론트가 멈추지 않게 기본값 반환
            return {
                "location": {"city": "통신에러", "district": "", "dong": ""},
                "weather": {"status": "Clear", "temp": 0, "description": "로드 실패", "icon": ""}
            }

    # 스키마(WeatherResponse) 형태에 맞춰 반환
    return {
        "location": { "city": city, "district": district, "dong": dong },
        "weather": {
            "status": status,
            "temp": temp,
            "description": weather_desc,
            "icon": ""
        }
    }