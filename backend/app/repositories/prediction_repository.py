from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.prediction import Prediction


class PredictionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, prediction_id: str) -> Optional[Prediction]:
        return self.db.query(Prediction).filter(Prediction.id == prediction_id).first()

    def get_by_user_id(
        self, user_id: str, limit: int = 10, offset: int = 0
    ) -> List[Prediction]:
        return (
            self.db.query(Prediction)
            .filter(Prediction.user_id == user_id)
            .order_by(Prediction.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def create(self, prediction_data: dict) -> Prediction:
        prediction = Prediction(
            user_id=prediction_data["user_id"],
            input_hash=prediction_data["input_hash"],
            input_data=prediction_data["input_data"],
            prediction_result=prediction_data["prediction_result"],
            confidence_score=prediction_data["confidence_score"],
            is_fallback_triggered=prediction_data.get("is_fallback_triggered", False),
        )
        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)
        return prediction

    def delete(self, prediction: Prediction) -> None:
        self.db.delete(prediction)
        self.db.commit()
