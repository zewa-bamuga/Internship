import enum
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

import pg

from app.domain.common.enums import UserStatuses
from app.domain.common.schemas import APIModel
from app.domain.storage.attachments.schemas import Attachment

from a8t_tools.db import pagination as pg
from a8t_tools.db import sorting as sr


class User(APIModel):
    id: UUID
    username: str
    status: UserStatuses
    avatar_attachment_id: UUID | None = None
    created_at: datetime


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


class UserDetails(User):
    avatar_attachment: Attachment | None = None


class UserCredentials(APIModel):
    username: str
    password: str


class UserDetailsFull(UserDetails):
    permissions: set[str] | None = None


class UserPartialUpdate(APIModel):
    username: str | None = None
    avatar_attachment_id: UUID | None = None
    permissions: set[str] | None = None
    status: str | None = None


class UserPartialUpdateFull(UserPartialUpdate):
    password_hash: str | None = None


class UserSorts(enum.StrEnum):
    id = enum.auto()
    username = enum.auto()
    status = enum.auto()
    created_at = enum.auto()


@dataclass
class UserListRequestSchema:
    pagination: pg.PaginationCallable[User] | None = None
    sorting: sr.SortingData[UserSorts] | None = None
