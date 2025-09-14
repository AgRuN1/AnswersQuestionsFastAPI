import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.config.database_helper import get_database_session

SQLITE_DATABASE_URL = "sqlite+aiosqlite:///./tests/test_db.db"

engine = create_async_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

testingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def remove_data():
    session = testingSessionLocal()
    await session.execute(text('''
        create table questions
        (
            id integer primary key autoincrement,
            text varchar not null,
            created_at timestamp not null
        );
    '''))
    await session.execute(text('''
        create table answers
        (
            id integer primary key autoincrement,
            text varchar not null,
            user_id uuid not null,
            question_id integer not null
                references questions
                    on delete cascade,
            created_at  timestamp not null
        );
    '''))
    await session.commit()
    yield 1
    await session.execute(text('DROP TABLE questions'))
    await session.execute(text('DROP TABLE answers'))
    await session.commit()
    await session.close()

@pytest_asyncio.fixture(scope="function")
async def db_session():
    session = testingSessionLocal()
    yield session
    await session.close()

@pytest.fixture(scope="function")
def test_client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_database_session] = override_get_db
    with TestClient(app) as test_client:
        yield test_client