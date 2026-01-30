from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import sys, os
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../../..')))
from app.db.base import Base
from app.core.config import DATABASE_URL

# 260104 김광원
# 생성되기를 원하는 테이블 반드시 이곳에 import 해줘야함 env.py에서 읽을 수 있게끔 
from app.models.user import User
from app.models.user_data import UserPreferredArtist, UserPreferredGenre

# 260104 김광원
# ini파일 대신 설정 (ini 파일 읽고 없으면 해당 설정값 적용되게 설정)
# 나머지 코드들은 alembic init시 적용되는 것들
config = context.config
if not config.get_main_option("sqlalchemy.url"):
    config.set_main_option("sqlalchemy.url", str(DATABASE_URL))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# 반드시 postgresql start 이후 실행
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
