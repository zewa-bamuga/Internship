from uuid import UUID

from a8t_tools.db.pagination import Paginated
from pydantic import EmailStr

from app.domain.common.exceptions import NotFoundError
from app.domain.users.core import schemas
from app.domain.users.core.repositories import UserRepository, SurveyRepository, UpdatePasswordRepository


class UserListQuery:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, payload: schemas.UserListRequestSchema) -> Paginated[schemas.User]:
        return await self.repository.get_users(payload.pagination, payload.sorting)


class UserRetrieveQuery:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, user_id: UUID) -> schemas.UserInternal:
        result = await self.repository.get_user_by_filter_or_none(schemas.UserWhere(id=user_id))
        if not result:
            raise NotFoundError()
        return schemas.UserInternal.model_validate(result)


class EmailRetrieveQuery:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, user_email: str) -> schemas.UserInternal:
        result = await self.repository.get_user_by_filter_by_email_or_none((schemas.UserWhere(email=user_email)))
        if not result:
            raise NotFoundError()
        return schemas.UserInternal.model_validate(result)


class SurveyListQuery:
    def __init__(self, repository: SurveyRepository):
        self.repository = repository

    async def __call__(self, payload: schemas.SurveyListRequestSchema) -> Paginated[schemas.Survey]:
        return await self.repository.get_surveys(payload.pagination, payload.sorting)


class UserRetrieveByUsernameQuery:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, username: str) -> schemas.UserInternal | None:
        return await self.repository.get_user_by_filter_or_none(schemas.UserWhere(username=username))


class UserRetrieveByEmailQuery:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, email: str) -> schemas.UserInternal | None:
        user_internal = await self.repository.get_user_by_filter_by_email_or_none(schemas.UserWhere(email=email))
        return user_internal


class UserRetrieveByCodeQuery:
    def __init__(self, repository: UpdatePasswordRepository):
        self.repository = repository

    async def __call__(self, code: str) -> schemas.PasswordResetCode | None:
        password_reset_code_internal = await self.repository.get_password_reset_code_by_code_or_none(
            schemas.PasswordResetCodeWhere(code=code))
        return password_reset_code_internal
