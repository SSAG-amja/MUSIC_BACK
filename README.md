# 1. tree structure

```
.
├── app
│   ├── api
│   │   └── v1                    # 버전별 API             
│   │       ├── endpoints         # 실제 라우터 (엔드포인트) 모아둔 dir
│   │       │   └── user.py
│   │       └── routers.py        # 해당 버전의 모든 라우터들 모아둔 모듈
│   ├── core
│   │   ├── config.py             # 환경변수 저장
│   │   └── security.py           # 세션 로직 등
│   ├── crud                      # DB 처리 로직
│   │   └── user.py               
│   ├── db                        
│   │   ├── alembic.ini.         
│   │   ├── base.py.              # Base = declarative_base()등
│   │   ├── migration             # Alembic 마이그레이션 폴더 - init 해야함 - document 참조
│   │   │   ├── env.py           
│   │   │   ├── README
│   │   │   ├── script.py.mako
│   │   │   └── versions
│   │   └── session.py            # DB 연결 엔진, 세션정리
│   ├── main.py
│   ├── models                    # SQLAlchemy 모델 정리
│   │   └── user.py
│   └── schemas                   # Pydantic 스키마
│       └── user.py
└── README.md
```

# 2. 요구사항(Prerequisites)
- Docker 환경에서 실행되도록 설계 Python, DB 설치 X

## 1. 다운로드
- [도커 다운로드](https://www.docker.com/products/docker-desktop/)

## 2. 환경변수설정(.env)
- .env_example 참조하여 설정

# 3. 실행방법

## 1. 서버 실행(Build & RUN)

```
# 이미지 빌드 및 실행(최초 실행시 라이브러리 추가 시 필수)
docker-compose up --build

# 이미지 있으면 아래 명령어로 실행
docker-compose up

# 백그라운드 실행
docker-compose up -d
```

## 2. 실행 확인
- Swagger UI (API 문서): http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 3. 백그라운드 실행중 로그 확인
```
# 전체 로그 보기
docker-compose logs -f

# 웹 혹은 DB 따로 확인 
docker-compose logs -f web
docker-compose logs -f db
```
- 종료시 : ctrl + c

## 4. 서버 중단 및 종료
```
# 잠시 멈춤
docker-compose stop

# 실행중인 터미널에서 종료
Ctrl + C

# 백그라운드 컨테이너까지 완전히 내리기
docker-compose down

# 초기화 : 컨테이너, 네트워크 등 데이터 모두 지움
docker-compose down -v
```

# 4. 데이터베이스 관리(Migration)
- 테이블 생성하거나 변경 사항 DB에 적용시 Docker Container 내부에서 alembic 실행해야함

## 1. 마이그레이션 적용(테이블 생성)
- DB 처음 실행 됐거나 모델 변경시 실행
```
# 1. 마이그레이션 파일 생성 (모델 변경 사항 감지)
docker-compose exec -w /back/app/db web alembic revision --autogenerate -m "[message]"

# 2. DB에 변경 사항 적용
docker-compose exec -w /back/app/db web alembic upgrade head

# WINDOWS 해당 명령어 사용
docker-compose exec -w //back/app/db web alembic upgrade head

# 3. 위 명령어 안될시 (직접 접속)
docker exec -it MUSIC_BACK /bin/bash 

cd app/db
alembic revision --autogenerate -m "[message]"
alembic upgrade head
```

## 2. DB 접속(CLI)
```
# docker exec -it [컨테이너이름] psql -U [유저명] -d [DB이름]
docker exec -it MUSIC_DB psql -U gookbob -d ssag_algo
```

# 5. 라이브러리 추가 방법
- requirements.txt 패키지 추가시, 반드시 이미지 다시 빌드

1. requirements.txt 수정
2. docker-compose up --build