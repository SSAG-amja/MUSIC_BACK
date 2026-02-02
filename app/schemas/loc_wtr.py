from pydantic import BaseModel

# 위치 정보 (Location)
class LocationData(BaseModel):
    city: str
    district: str
    dong: str

# 날씨 정보 (Weather)
class WeatherData(BaseModel):
    status: str
    temp: float
    description: str
    icon: str

# 최종 응답 (Response)
class WeatherResponse(BaseModel):
    location: LocationData
    weather: WeatherData