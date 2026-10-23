from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from app.core.config import settings

# Transformamos la URL de postgresql:// a postgresql+asyncpg:// para soporte asíncrono
DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Creamos el motor asíncrono de SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=settings.DEBUG, future=True)

# Fábrica de sesiones asíncronas para las peticiones de FastAPI
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency para inyectar sesiones de base de datos en los endpoints."""
    async with AsyncSessionLocal() as session:
        yield session