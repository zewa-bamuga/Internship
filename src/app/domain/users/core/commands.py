import datetime
import secrets
import uuid
from uuid import UUID

from fastapi import HTTPException
from loguru import logger
from pydantic import EmailStr

from app.domain.common import enums
from app.domain.common.models import PasswordResetCode
from app.domain.users.core import schemas
from app.domain.users.core.queries import UserRetrieveByUsernameQuery, UserRetrieveByEmailQuery, UserRetrieveByCodeQuery
from app.domain.users.core.repositories import UserRepository, SurveyRepository, QuestionRepository, \
    UpdatePasswordRepository
from app.domain.users.core.schemas import UpdatePasswordRequest, UpdatePasswordConfirm, UserProfilePartialUpdate, \
    UserPartialUpdateFull
from app.domain.users.registration.hi import send_password_reset_email


class SurveyCreateCommand:
    def __init__(
            self,
            repository: SurveyRepository,
    ):
        self.repository = repository

    async def __call__(self, payload: schemas.SurveyCreate) -> None:
        survey_id_container = await self.repository.create_survey(
            schemas.SurveyCreate(
                **payload.model_dump(),
            )
        )
        logger.info("Survey created: {survey_id}", survey_id=survey_id_container.id)


class QuestionCreateCommand:
    def __init__(
            self,
            repository: QuestionRepository,
    ):
        self.repository = repository

    async def __call__(self, payload: schemas.QuestionCreate) -> None:
        question_id_container = await self.repository.create_question(
            schemas.QuestionCreate(
                **payload.model_dump(),
            )
        )
        logger.info("Question created: {question_id}", question_id=question_id_container.id)


class UpdatePasswordRequestCommand:
    def __init__(
            self,
            user_retrieve_by_email_query: UserRetrieveByEmailQuery,
            repository: UpdatePasswordRepository,
    ):
        self.user_retrieve_by_email_query = user_retrieve_by_email_query
        self.repository = repository

    async def __call__(self, payload: schemas.UpdatePasswordRequest) -> UpdatePasswordRequest:
        email = payload.email
        user_internal = await self.user_retrieve_by_email_query(email)

        user_id = user_internal.id
        code = PasswordResetCode.generate_code()
        password_reset_code = schemas.PasswordResetCode(
            user_id=user_id,
            code=code,
        )
        password_reset_code_id_container = await self.repository.create_update_password(password_reset_code)
        await send_password_reset_email(email, code)
        logger.info("Password reset code created: {password_reset_code_id}",
                    password_reset_code_id=password_reset_code_id_container.id)

        return UpdatePasswordRequest(email=email)


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


class UpdatePasswordConfirmCommand:
    def __init__(
            self,
            user_retrieve_by_email_query: UserRetrieveByEmailQuery,
            user_retrieve_by_code_query: UserRetrieveByCodeQuery,
            repository: UserRepository,
            user_partial_update_command: UserPartialUpdateCommand,
    ):
        self.user_retrieve_by_email_query = user_retrieve_by_email_query
        self.user_retrieve_by_code_query = user_retrieve_by_code_query
        self.repository = repository
        self.user_partial_update_command = user_partial_update_command

    async def __call__(self, payload: schemas.UserProfilePartialUpdate) -> None:
        email = payload.email
        user_internal = await self.user_retrieve_by_email_query(email)

        code = payload.code
        code_internal = await self.user_retrieve_by_code_query(code)

        user_id = user_internal.id
        user_id_by_code = code_internal.user_id

        password = payload.password

        print(user_id, user_id_by_code, password)

        await self.user_partial_update_command(
            user_id, UserPartialUpdateFull(**payload.model_dump(exclude_unset=True))
        )


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


class UserActivateCommand:
    def __init__(
            self,
            repository: UserRepository,
    ):
        self.repository = repository

    async def __call__(self, user_id: UUID) -> None:
        await self.repository.set_user_status(user_id, enums.UserStatuses.active)
