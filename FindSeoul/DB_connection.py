#추후삭제
from dotenv import load_dotenv
load_dotenv('.env')

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1) 환경변수나 설정에서 DB URL 읽기
schema_name = 'seouldata'

connection_string = os.getenv('DB_URI')

# 2) 엔진 생성 (커넥션 풀 설정 포함)
engine = create_engine(
    connection_string,
    pool_size=10,         # 기본 풀 크기
    max_overflow=20,      # 풀 초과 커넥션 수
    pool_pre_ping=True,   # 사용 전 ping 검사
    pool_recycle=3600     # 초단위 재활용 주기
)

# 3) 세션팩토리 정의
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

