from pydantic import BaseModel

# 260117 김광원
# 토큰 스키마 
class Token(BaseModel):
    access_token: str
    token_type: str