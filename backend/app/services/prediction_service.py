from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.sanitizer import sanitize_input_payload
from app.models.prediction import Prediction
from app.repositories.prediction_repository import PredictionRepository
from app.schemas.prediction import PredictionRequest
from app.services.ai_service import AIService


class PredictionService:
    def __init__(self, db: Session):
        self.db = db
        self.prediction_repo = PredictionRepository(db)
        self.ai_service = AIService()

    def create_prediction(self, request: PredictionRequest, current_user_id: str) -> Prediction:
        """
        Creates a new AI prediction:
        1. Sanitizes input payload against prompt injection and malicious structures.
        2. Computes input SHA-256 hash.
        3. Executes AI demand forecast inference with fallback support.
        4. Saves result mapped to the authenticated user ID.
        """
        clean_input = sanitize_input_payload(request.input_data)
        input_hash = self.ai_service.compute_input_hash(clean_input)
        prediction_result, confidence_score, is_fallback = self.ai_service.predict_demand(clean_input)

        prediction_record = self.prediction_repo.create({
            "user_id": current_user_id,
            "input_hash": input_hash,
            "input_data": clean_input,
            "prediction_result": prediction_result,
            "confidence_score": confidence_score,
            "is_fallback_triggered": is_fallback,
        })
        return prediction_record

    def get_user_predictions(
        self, current_user_id: str, limit: int = 10, offset: int = 0
    ) -> List[Prediction]:
        """
        Retrieves paginated prediction history strictly scoped to current_user_id.
        Prevents IDOR/BOLA by ensuring tenant boundary.
        """
        # Upper limit check against API4: Unrestricted Resource Consumption
        safe_limit = min(max(1, limit), 100)
        safe_offset = max(0, offset)
        return self.prediction_repo.get_by_user_id(
            user_id=current_user_id, limit=safe_limit, offset=safe_offset
        )

    def get_prediction_by_id(self, prediction_id: str, current_user_id: str) -> Prediction:
        """
        Retrieves a prediction by ID with strict OWASP API1:2023 (Anti-BOLA) check.
        If the record does not belong to current_user, raises HTTP 403 Forbidden.
        """
        prediction = self.prediction_repo.get_by_id(prediction_id)
        if not prediction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Data prediksi dengan ID tersebut tidak ditemukan.",
            )

        # OWASP API1:2023 BOLA Check
        if prediction.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Akses ditolak. Anda tidak memiliki izin untuk mengakses resource prediksi milik pengguna lain (BOLA Protection).",
            )

        return prediction
