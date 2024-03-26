from uuid import UUID

from src.app.domain.common.schemas import APIModel


class UserProfilePartialUpdate(APIModel):
    username: str | None = None
    password: str | None = None
    avatar_attachment_id: UUID | None = None
