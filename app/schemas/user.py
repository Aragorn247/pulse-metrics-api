from typing import Optional
from pydantic import BaseModel, EmailStr

# Propiedades compartidas base
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

# Propiedades que se reciben al crear un usuario (Registro)
class UserCreate(UserBase):
    email: EmailStr
    password: str

# Propiedades que se reciben al actualizar un usuario
class UserUpdate(UserBase):
    password: Optional[str] = None

# Propiedades que se devuelven al cliente (Oculta la contraseña)
class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str