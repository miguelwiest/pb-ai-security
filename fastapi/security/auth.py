import os
from datetime import datetime, timedelta, timezone
from typing import Optional
import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from models.schemas import User, UserInDB

# Configurações de Segurança do JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "pb_infnet_super_secret_jwt_key_2026_x9a8b7c6")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Esquema de autenticação OAuth2PasswordBearer
# O tokenUrl aponta para a rota POST /auth/token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_password_hash(password: str) -> str:
    """Gera o hash seguro de uma senha usando bcrypt."""
    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto plano corresponde ao hash armazenado."""
    pwd_bytes = plain_password.encode("utf-8")[:72]
    return bcrypt.checkpw(pwd_bytes, hashed_password.encode("utf-8"))


# ==============================================================================
# BASE DE USUÁRIOS IN-CODE (ADMIN EXCLUSIVO CONFORME ESPECIFICAÇÃO DO ENUNCIADO)
# ==============================================================================
ADMIN_PASSWORD_PLAIN = "AdminInfnet2026!"
ADMIN_PASSWORD_HASH = get_password_hash(ADMIN_PASSWORD_PLAIN)

USERS_DB: dict[str, UserInDB] = {
        "admin": UserInDB(
            username="admin",
            email="admin@infnet.edu.br",
            full_name="Administrador do Atendimento IA",
            disabled=False,
            hashed_password=ADMIN_PASSWORD_HASH
        )
}


def get_user(db: dict, username: str) -> Optional[UserInDB]:
    """Recupera os dados de um usuário na base in-code."""
    if username in db:
        return db[username]
    return None


def authenticate_user(db: dict, username: str, password: str) -> Optional[UserInDB]:
    """Autentica o usuário validando login e senha."""
    user = get_user(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Gera um novo token JWT codificado com expiração."""
    to_encode = data.copy()
    now_utc = datetime.now(timezone.utc)
    if expires_delta:
        expire = now_utc + expires_delta
    else:
        expire = now_utc + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": now_utc})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """Decodifica, valida e extrai 'sub' presente no header do token JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        return username
    except jwt.PyJWTError:
        return None


async def get_token_user(token: str = Depends(oauth2_scheme)) -> User:
    """Dependência FastAPI que extrai e valida o usuário a partir do token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado/ausente",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = verify_token(token)
    if username is None:
        raise credentials_exception
    user = get_user(USERS_DB, username)
    if user is None:
        raise credentials_exception
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    return User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        disabled=user.disabled
    )