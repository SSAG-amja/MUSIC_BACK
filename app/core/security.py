# app/core/security.py
import bcrypt

# 260116 김광원
# 비밀번호 확인 (평문과 DB 비밀번호 비교)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # bcrypt는 bytes 타입 필요하여 encode() 수행
    # DB에서 꺼낸 hashed_password가 str이라면 bytes로 변환해야 합니다.
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

# 260116 김광원
# 비밀번호 해싱
def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    
    # salt 생성 및 해싱
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
    
    # DB 저장을 위해 bytes를 다시 string으로 변환해서 반환
    return hashed_bytes.decode('utf-8')