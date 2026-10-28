from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import AsyncSessionLocal
from app.core.config import settings
from app.core.security import ALGORITHM
from app.models.user import User
from app.schemas.token import TokenPayload

# Esquema OAuth2 para extraer el token del header Authorization: Bearer <token>
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/api/v1/login/access-token"
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependencia para obtener una sesión de base de datos asíncrona por petición."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> User:
    """Valida el token JWT y retorna el usuario autenticado actual."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        secret_key = getattr(settings, "SECRET_KEY", "SUPER_SECRET_KEY_CHANGEME_IN_PRODUCTION")
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        token_data = TokenPayload(sub=payload.get("sub"))
        if token_data.sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Buscamos el usuario en la base de datos asíncrona
    result = await db.execute(select(User).filter(User.id == int(token_data.sub)))
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo"
        )
        
    return user