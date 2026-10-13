from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRegisterRequest(BaseModel):
    full_name: str = Field(..., json_schema_extra={"example": "Ahmad Dahlan"})
    email: EmailStr = Field(..., json_schema_extra={"example": "ahmad@example.com"})
    password: str = Field(..., min_length=8, json_schema_extra={"example": "SecurePass123!"})


class UserLoginRequest(BaseModel):
    email: EmailStr = Field(..., json_schema_extra={"example": "ahmad@example.com"})
    password: str = Field(..., json_schema_extra={"example": "SecurePass123!"})


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
