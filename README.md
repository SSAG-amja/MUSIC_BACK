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

# 2. 실행방법

1. 프로젝트 폴더로 이동

2. 가상환경 생성 (최초 1번)
```
python -m venv venv
```

3. 가상환경 켜기
- linux, Mac
```
source venv/bin/activate
```

- windows
```
# git bash
source venv/Scripts/activate

# PowerShell / CMD
.\venv\Scripts\activate
```

4. 라이브러리 설치
```
pip install -r requirements.txt
```

5. .env 파일 설정
- 루트 디렉토리에 생성

6. 실행
```
python -m uvicorn app.main:app --reload
```