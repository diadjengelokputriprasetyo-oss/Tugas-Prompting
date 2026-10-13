from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserRegisterRequest, UserLoginRequest, UserResponse
from app.schemas.token import TokenResponse, TokenRefreshRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Pendaftaran Pengguna Baru",
)
@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,  # Alias for prompt compatibility
)
def register(
    data: UserRegisterRequest,
    db: Session = Depends(get_db),
):
    """
    Mendaftarkan pengguna baru dengan validasi schema, pengecekan email unik,
    dan enkripsi password menggunakan bcrypt.
    """
    service = AuthService(db)
    return service.register(data)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Otentikasi Pengguna & Buat Token",
)
def login(
    data: UserLoginRequest,
    db: Session = Depends(get_db),
):
    """
    Memverifikasi kredensial pengguna dan mengembalikan pasangan token JWT
    (Access Token 30m + Refresh Token 7d).
    """
    service = AuthService(db)
    return service.login(data)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh Access Token",
)
def refresh_token(
    data: TokenRefreshRequest,
    db: Session = Depends(get_db),
):
    """
    Menerbitkan Access Token baru menggunakan Refresh Token yang valid.
    """
    service = AuthService(db)
    return service.refresh(data.refresh_token)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Profil Pengguna yang Sedang Login",
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Protected endpoint untuk melihat profil pengguna yang sedang login.
    Menolak request tanpa Authorization: Bearer <token> (HTTP 401).
    """
    return current_user
