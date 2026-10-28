from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Contexto para el hash de contraseñas usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña en texto plano coincide con su hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera el hash seguro de una contraseña."""
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """Crea un token JWT de acceso con tiempo de expiración configurable."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15) # Por defecto 15 minutos de seguridad
    
    to_encode = {"exp": expire, "sub": str(subject)}
    
    # Nota: Asegúrate de tener una clave secreta segura en tus settings, 
    # o usa una por defecto si estás en desarrollo local.
    secret_key = getattr(settings, "SECRET_KEY", "SUPER_SECRET_KEY_CHANGEME_IN_PRODUCTION")
    
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt