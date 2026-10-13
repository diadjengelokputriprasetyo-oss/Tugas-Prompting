from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    code: int = Field(..., json_schema_extra={"example": 400})
    message: str = Field(..., json_schema_extra={"example": "Permintaan tidak valid atau data gagal diproses."})


class MessageResponse(BaseModel):
    message: str = Field(..., json_schema_extra={"example": "Operasi berhasil dilakukan."})
