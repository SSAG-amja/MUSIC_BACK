from fastapi import APIRouter, HTTPException
import httpx
# [변경 1] config에서 필요한 키만 직접 Import
from app.core.config import KAKAO_REST_API_KEY, OPENWEATHERMAP_API_KEY
from app.schemas.loc_wtr import WeatherResponse 

router = APIRouter()

# 260203 김호영
# 위치 및 날씨 조회 API 작성 (OpenWeatherMap 버전)
@router.get("/getLocWtr", response_model=WeatherResponse)
async def get_location_and_weather(lat: float, lon: float):
    
    # [변경 2] config.변수명 접근이나 재할당 없이, import한 변수를 검증에 바로 사용
    if not KAKAO_REST_API_KEY or not OPENWEATHERMAP_API_KEY:
        print("❌ [ERROR] API Key Missing in config.py")
        raise HTTPException(status_code=500, detail="Server Configuration Error")

    async with httpx.AsyncClient() as client:
        try:
            # -------------------------------------------------
            # [A] 카카오: 좌표 -> 주소
            # -------------------------------------------------
            # [변경 3] Authorization 헤더에 직접 Import한 키 사용
            kakao_res = await client.get(
                "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json",
                headers={"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}, 
                params={"x": lon, "y": lat} 
            )
            kakao_res.raise_for_status()
            kakao_data = kakao_res.json()
            
            city, district, dong = "위치미상", "", ""
            if kakao_data.get('documents'):
                addr = kakao_data['documents'][0]
                city = addr['region_1depth_name']
                district = addr['region_2depth_name']
                dong = addr['region_3depth_name']

            # -------------------------------------------------
            # [B] OpenWeatherMap: 좌표 -> 날씨
            # -------------------------------------------------
            # [변경 4] appid 파라미터에 직접 Import한 키 사용
            owm_res = await client.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": OPENWEATHERMAP_API_KEY, 
                    "units": "metric",
                    "lang": "kr"
                }
            )
            owm_res.raise_for_status()
            owm_data = owm_res.json()

            # 로그 확인 (필요시 주석 해제)
            # print("================ OWM 날씨 원본 데이터 ================")
            # print(owm_data) 
            # print("======================================================")

            # 1. 기본 데이터 추출
            temp = owm_data["main"]["temp"]
            weather_desc = owm_data["weather"][0]["description"]
            weather_main = owm_data["weather"][0]["main"]
            icon_code = owm_data["weather"][0]["icon"]

            # 2. 상태 매핑
            status = "Clear"
            
            if weather_main in ["Thunderstorm", "Drizzle", "Rain"]:
                status = "Rain"
            elif weather_main == "Snow":
                status = "Snow"
            elif weather_main == "Clouds":
                status = "Clouds"
            elif weather_main in ["Mist", "Smoke", "Haze", "Dust", "Fog", "Sand", "Ash", "Squall", "Tornado"]:
                status = "Atmosphere"
            else:
                status = "Clear"

        except Exception as e:
            print(f"❌ API Error: {e}")
            return {
                "location": {"city": "통신에러", "district": "", "dong": ""},
                "weather": {"status": "Clear", "temp": 0, "description": "로드 실패", "icon": ""}
            }

    return {
        "location": { "city": city, "district": district, "dong": dong },
        "weather": {
            "status": status,
            "temp": temp,
            "description": weather_desc,
            "icon": f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        }
    }