from src.app.domain.common import enums
from src.app.domain.common.schemas import APIModel


class SimpleApiError(APIModel):
    code: enums.ErrorCodes
    message: str


class AuthApiErrorPayload(APIModel):
    code: enums.AuthErrorCodes


class AuthApiError(SimpleApiError):
    payload: AuthApiErrorPayload
