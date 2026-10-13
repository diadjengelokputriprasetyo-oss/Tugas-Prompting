from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.prediction_service import PredictionService

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.post(
    "",
    response_model=PredictionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Buat Prediksi Baru (Model AI)",
)
def create_prediction(
    request: PredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Memproses data masukan melalui model AI AutoPartSmart dengan sanitasi keamanan,
    perhitungan confidence score, dan fallback otomatis.
    """
    service = PredictionService(db)
    return service.create_prediction(request, current_user.id)


@router.get(
    "",
    response_model=List[PredictionResponse],
    status_code=status.HTTP_200_OK,
    summary="Ambil Riwayat Prediksi Pengguna",
)
def get_prediction_history(
    limit: int = Query(10, ge=1, le=100, description="Jumlah maksimum data yang dikembalikan"),
    offset: int = Query(0, ge=0, description="Jumlah data yang dilewati untuk paginasi"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Mendapatkan daftar riwayat prediksi terpaginasi milik pengguna yang sedang login.
    Menerapkan pemisahan batas data antar pengguna untuk mencegah kebocoran data.
    """
    service = PredictionService(db)
    return service.get_user_predictions(current_user.id, limit=limit, offset=offset)


@router.get(
    "/{prediction_id}",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Detail Hasil Prediksi",
)
def get_prediction_by_id(
    prediction_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Mengambil rincian prediksi berdasarkan ID spesifik.
    Memiliki verifikasi kepemilikan objek ketat (Anti-BOLA/IDOR).
    Jika data bukan milik pengguna yang login, sistem menolak dengan HTTP 403 Forbidden.
    """
    service = PredictionService(db)
    return service.get_prediction_by_id(prediction_id, current_user.id)
