from typing import Optional
from uuid import UUID

from a8t_tools.bus.producer import TaskProducer
from a8t_tools.security.hashing import PasswordHashService
from loguru import logger

from app.domain.common import enums
from app.domain.common.schemas import IdContainer
# from app.domain.common.models import PasswordResetCode
from app.domain.users.core import schemas
from app.domain.users.core.repositories import UserRepository
from app.domain.users.core.schemas import UserDetails
from app.domain.users.registration.hi import EmailService


class UserCreateCommand:
    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    async def __call__(self, payload: schemas.UserCreate) -> schemas.UserDetails:
        user_id_container = await self.repository.create_user(
            schemas.UserCreateFull(
                status=enums.UserStatuses.unconfirmed,
                **payload.model_dump(),
            )
        )
        logger.info("User created: {user_id}", user_id=user_id_container.id)
        user = await self.repository.get_user_by_filter_or_none(schemas.UserWhere(id=user_id_container.id))
        assert user
        return schemas.UserDetails.model_validate(user)


class UserPartialUpdateCommand:
    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    async def __call__(self, user_id: UUID, payload: schemas.UserPartialUpdateFull) -> schemas.UserDetailsFull:
        await self.repository.partial_update_user(user_id, payload)
        user = await self.repository.get_user_by_filter_or_none(schemas.UserWhere(id=user_id))
        assert user
        return schemas.UserDetailsFull.model_validate(user)


class UserActivateCommand:
    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    async def __call__(self, user_id: UUID) -> None:
        await self.repository.set_user_status(user_id, enums.UserStatuses.active)
