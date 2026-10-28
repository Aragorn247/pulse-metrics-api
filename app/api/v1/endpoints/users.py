from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api import deps
from app.core.security import get_password_hash
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate

router = APIRouter()

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """Crea un nuevo usuario en el sistema con la contraseña encriptada."""
    
    # Verificamos si ya existe un usuario registrado con ese email
    result = await db.execute(select(UserModel).filter(UserModel.email == user_in.email))
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario registrado con este correo electrónico.",
        )
    
    # Creamos el modelo de base de datos cifrando la contraseña
    db_obj = UserModel(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser,
    )
    
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    
    return db_obj