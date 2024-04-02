from uuid import UUID

from pydantic import EmailStr

from app.domain.common.schemas import APIModel


class UserProfilePartialUpdate(APIModel):
    email: EmailStr | None = None
    password: str | None = None
    avatar_attachment_id: UUID | None = None
