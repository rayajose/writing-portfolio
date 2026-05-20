import os

from cryptography.fernet import Fernet
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from settings import Settings, get_settings

api_key_header = APIKeyHeader(
    name="x-api-key",
    scheme_name="APIKeyAuth",
    description="API key required to access this API.",
)


def require_api_key(
    api_key: str = Depends(api_key_header),
    settings: Settings = Depends(get_settings),
) -> str:
    if api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing API key"
        )

    return api_key


PII_ENCRYPTION_KEY = os.getenv("PII_ENCRYPTION_KEY")

if not PII_ENCRYPTION_KEY:
    raise RuntimeError("PII_ENCRYPTION_KEY environment variable is not set.")

pii_cipher = Fernet(PII_ENCRYPTION_KEY.encode())


def encrypt_pii(value: str | None) -> str | None:
    if value is None:
        return None

    return pii_cipher.encrypt(value.encode()).decode()


def decrypt_pii(value: str | None) -> str | None:
    if value is None:
        return None

    return pii_cipher.decrypt(value.encode()).decode()


def mask_email(email: str | None) -> str | None:
    if email is None:
        return None

    if "@" not in email:
        return "***"

    name, domain = email.split("@", 1)

    visible = name[:2]

    return f"{visible}***@{domain}"


def mask_phone(phone: str | None) -> str | None:
    if phone is None:
        return None

    digits = "".join(ch for ch in phone if ch.isdigit())

    if len(digits) < 4:
        return "***"

    return f"***-***-{digits[-4:]}"


def mask_postal_code(postal_code: str | None) -> str | None:
    if postal_code is None:
        return None

    if len(postal_code) <= 2:
        return "***"

    return f"***{postal_code[-2:]}"


def mask_address_line1(address: str | None) -> str | None:
    if address is None:
        return None

    parts = address.split(" ", 1)

    if len(parts) == 1:
        return "***"

    return f"{parts[0]} ***"
