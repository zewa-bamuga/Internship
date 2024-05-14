from a8t_tools.db.pagination import Paginated

from app.domain.users.core.queries import SurveyListQuery
from app.domain.users.core.schemas import SurveyListRequestSchema, Survey
from app.domain.users.permissions.schemas import BasePermissions
from app.domain.users.permissions.services import UserPermissionService


class SurveyManagementListQuery:
    def __init__(self, permission_service: UserPermissionService, query: SurveyListQuery) -> None:
        self.query = query
        self.permission_service = permission_service

    async def __call__(self, payload: SurveyListRequestSchema) -> Paginated[Survey]:
        await self.permission_service.assert_permissions(BasePermissions.superuser)
        return await self.query(payload)
