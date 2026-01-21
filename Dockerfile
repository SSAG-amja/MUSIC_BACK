# 1. 파이썬 3.13 슬림 이미지 사용 (가볍고 빠름)
FROM python:3.13-slim

# 2. 작업 디렉토리 설정
WORKDIR /back

# 3. 환경 변수 설정 (파이썬 버퍼링 비활성화 등)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. 의존성 설치를 위해 requirements.txt 복사
COPY ./requirements.txt /back/requirements.txt

# 5. 패키지 설치
RUN pip install --no-cache-dir --upgrade -r /back/requirements.txt

# 6. 소스 코드 전체 복사
COPY ./app /back/app

# 7. 실행 명령어 (호스트 0.0.0.0 설정 필수)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]