from uuid import UUID

from a8t_tools.db import pagination, sorting
from dependency_injector import wiring
from fastapi import APIRouter, Depends, UploadFile

from app.api import deps
from app.containers import Container
from app.domain.storage.attachments import schemas
from app.domain.storage.attachments.commands import AttachmentCreateCommand
from app.domain.storage.attachments.queries import (
    AttachmentListQuery,
    AttachmentRetrieveQuery,
)

router = APIRouter()
