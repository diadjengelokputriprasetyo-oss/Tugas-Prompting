from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRegisterRequest, UserLoginRequest
from app.schemas.token import TokenResponse


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, data: UserRegisterRequest) -> User:
        """
        Registers a new user:
        1. Checks for duplicate email.
        2. Hashes password using bcrypt.
        3. Persists user via UserRepository.
        """
        existing_user = self.user_repo.get_by_email(data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email sudah terdaftar dalam sistem.",
            )

        hashed = hash_password(data.password)
        user = self.user_repo.create({
            "full_name": data.full_name.strip(),
            "email": data.email.lower().strip(),
            "password_hash": hashed,
        })
        return user

    def login(self, data: UserLoginRequest) -> TokenResponse:
        """
        Authenticates user with email and password:
        1. Verifies user existence and bcrypt hash.
        2. Returns access token (30m) and refresh token (7d).
        """
        user = self.user_repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email atau kata sandi tidak valid.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    def refresh(self, refresh_token_str: str) -> TokenResponse:
        """
        Validates refresh token and issues a new access token.
        """
        try:
            payload = decode_token(refresh_token_str)
            token_type = payload.get("type")
            if token_type != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token yang diberikan bukan refresh token.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Subjek token tidak ditemukan.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token tidak valid atau telah kadaluwarsa.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Pengguna tidak ditemukan.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        new_access_token = create_access_token(subject=user.id)
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=refresh_token_str,
            token_type="bearer",
        )
