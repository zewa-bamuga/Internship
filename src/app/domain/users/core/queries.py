from uuid import UUID

from a8t_tools.db.pagination import Paginated

from app.domain.common.exceptions import NotFoundError
from app.domain.users.core import schemas
from app.domain.users.core.repositories import UserRepository


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


class UserRetrieveByUsernameQuery:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, username: str) -> schemas.UserInternal | None:
        return await self.repository.get_user_by_filter_or_none(schemas.UserWhere(username=username))
