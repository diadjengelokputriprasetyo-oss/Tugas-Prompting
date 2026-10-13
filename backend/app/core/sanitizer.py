import re
import html
from typing import Any, Dict
from fastapi import HTTPException, UploadFile, status
from app.core.config import settings

# Patterns for prompt injection, malicious commands, script tags, control chars
DANGEROUS_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+instructions?", re.IGNORECASE),
    re.compile(r"system\s*override", re.IGNORECASE),
    re.compile(r"<script.*?>.*?</script>", re.IGNORECASE | re.DOTALL),
    re.compile(r"javascript:", re.IGNORECASE),
    re.compile(r"(\.\./|\.\.\\)", re.IGNORECASE),  # Path traversal
]

# Control characters regex (excluding standard whitespace \t, \n, \r)
CONTROL_CHARS_PATTERN = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")


def sanitize_string(text: str) -> str:
    """
    Sanitize text input:
    1. Strip control characters.
    2. Check against known prompt injection and command injection patterns.
    3. HTML escape to mitigate injection payloads.
    """
    if not isinstance(text, str):
        return text

    # Remove non-printable control characters
    cleaned = CONTROL_CHARS_PATTERN.sub("", text).strip()

    # Detect prompt injection attempts
    for pattern in DANGEROUS_PATTERNS:
        if pattern.search(cleaned):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Deteksi masukan berbahaya atau upaya manipulasi instruksi (Prompt Injection).",
            )

    # HTML escape dangerous characters
    return html.escape(cleaned)


def sanitize_input_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively sanitize input dictionary for AI inference.
    Validates data types and removes malicious characters from string fields.
    """
    if not isinstance(data, dict):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Payload input_data harus berupa dictionary objek JSON.",
        )

    sanitized: Dict[str, Any] = {}
    for key, value in data.items():
        # Sanitize key
        clean_key = sanitize_string(str(key))
        if isinstance(value, str):
            sanitized[clean_key] = sanitize_string(value)
        elif isinstance(value, (int, float, bool)) or value is None:
            sanitized[clean_key] = value
        elif isinstance(value, dict):
            sanitized[clean_key] = sanitize_input_payload(value)
        elif isinstance(value, list):
            sanitized[clean_key] = [
                sanitize_string(item) if isinstance(item, str) else item
                for item in value
            ]
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Tipe data field '{clean_key}' tidak didukung.",
            )

    return sanitized


async def validate_upload_file(file: UploadFile) -> None:
    """
    Validates uploaded file against OWASP API4 (Unrestricted Resource Consumption)
    and malicious MIME injection:
    - Maximum size <= settings.MAX_FILE_SIZE_MB (default 5MB)
    - MIME whitelist check
    - File extension validation
    """
    # 1. MIME Whitelisting
    if file.content_type not in settings.ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Tipe MIME '{file.content_type}' tidak diizinkan. Tipe yang diperbolehkan: {settings.ALLOWED_MIME_TYPES}",
        )

    # 2. Extension validation
    filename = file.filename or ""
    has_valid_ext = any(filename.lower().endswith(ext) for ext in settings.ALLOWED_EXTENSIONS)
    if not has_valid_ext:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Ekstensi berkas tidak valid. Format yang didukung: {settings.ALLOWED_EXTENSIONS}",
        )

    # 3. File size check (read in chunks up to max allowed bytes)
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    content = await file.read()
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Ukuran berkas melebihi batas maksimum {settings.MAX_FILE_SIZE_MB}MB.",
        )

    # Reset cursor for downstream readers
    await file.seek(0)
