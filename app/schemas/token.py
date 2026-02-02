from pydantic import BaseModel

# 260117 김광원
# 토큰 스키마 
class Token(BaseModel):
    access_token: str
    token_type: str

# 260131 김광원
# 로그인시 신규유저인지 확인
class LoginRespose(Token):
    is_newer: bool