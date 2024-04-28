from typing import Optional
from uuid import UUID

from a8t_tools.security.hashing import PasswordHashService
from loguru import logger

from app.domain.common import enums
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


# class PasswordResetService:
#     def __init__(
#             self,
#             repository: UserRepository,
#             # email_service: EmailService,
#             password_hash_service: PasswordHashService,
#     ):
#         self.repository = repository
#         # self.email_service = email_service
#         self.password_hash_service = password_hash_service
#
#     async def reset_password(self, email: str) -> Optional[UserDetails]:
#         user = await self.repository.get_user_by_email(email)
#         if not user:
#             return None
#
#         # Create an instance of PasswordResetCode
#         password_reset_code = PasswordResetCode()
#
#         # Generate code using the instance method
#         code = password_reset_code.generate_code()
#
#         # Save code to the database and send it to the user
#         await self.repository.save_password_reset_code(user.id, code)
#         await self.email_service.send_password_reset_email(user.email, code)
#
#         return user
