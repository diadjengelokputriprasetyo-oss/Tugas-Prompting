from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel, Field, ConfigDict


class PredictionRequest(BaseModel):
    input_data: Dict[str, Any] = Field(
        ...,
        description="Payload fitur acuan untuk inferensi AI AutoPartSmart (misal: item_id, lag_1, lag_2, lag_3)",
        json_schema_extra={"example": {"item_id": "A-04000-081B0", "lag_1": 8, "lag_2": 6, "lag_3": 5}},
    )


class PredictionResponse(BaseModel):
    id: str
    user_id: str
    input_hash: str
    prediction_result: Dict[str, Any]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    is_fallback_triggered: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
