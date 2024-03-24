from uuid import UUID

from src.app.domain.common.schemas import APIModel


class UserCreate(APIModel):
    username: str
    password_hash: str
    avatar_attachment_id: UUID | None = None
    permission: set[str] | None = None
