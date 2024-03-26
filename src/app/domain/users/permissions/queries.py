from uuid import UUID

from src.app.domain.users.core.queries import UserRetrieveQuery
from src.app.domain.users.permissions.schemas import BasePermissions


class UserPermissionListQuery:
    def __init__(self, query: UserRetrieveQuery) -> None:
        self.query = query

    async def __call__(self, user_id: UUID) -> set[str]:
        user = await self.query(user_id)
        return (user.permissions or set()) | {BasePermissions.authenticated}
