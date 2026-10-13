from typing import Optional
from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str = Field(..., json_schema_extra={"example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."})
    refresh_token: Optional[str] = Field(None, json_schema_extra={"example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."})
    token_type: str = Field(default="bearer", json_schema_extra={"example": "bearer"})


class TokenRefreshRequest(BaseModel):
    refresh_token: str = Field(..., json_schema_extra={"example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."})


class TokenPayload(BaseModel):
    sub: str
    type: str
    exp: int
    iat: int
