from uuid import UUID
from datetime import datetime

from src.app.domain.common.enums import UserStatuses
from src.app.domain.common.schemas import APIModel
from src.app.domain.storage.attachments.schemas import Attachment


class UserCreate(APIModel):
    username: str
    password_hash: str
    avatar_attachment_id: UUID | None = None
    permission: set[str] | None = None


class UserInternal(APIModel):
    id: UUID
    username: str
    password_hash: str
    permissions: set[str] | None = None
    avatar_attachment_id: UUID | None = None
    avatar_attachment: Attachment | None = None
    status: UserStatuses
    created_at: datetime
