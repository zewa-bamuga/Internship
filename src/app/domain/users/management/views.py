from uuid import UUID

from dependency_injector import wiring
from fastapi import APIRouter, Depends

from app.api import deps
from app.containers import Container
from app.domain.users.core import schemas
from app.domain.users.management.commands import (
    UserManagementCreateCommand,
    UserManagementPartialUpdateCommand,
)
from app.domain.users.management.queries import (
    UserManagementListQuery,
    UserManagementRetrieveQuery,
)
from a8t_tools.db import pagination, sorting

router = APIRouter()


@router.get(
    "",
    response_model=pagination.CountPaginationResults[schemas.User],
)
@wiring.inject
async def get_users_list(
    query: UserManagementListQuery = Depends(wiring.Provide[Container.user.management_list_query]),
    pagination: pagination.PaginationCallable[schemas.User] = Depends(deps.get_skip_limit_pagination_dep(schemas.User)),
    sorting: sorting.SortingData[schemas.UserSorts] = Depends(
        deps.get_sort_order_sorting_dep(
            schemas.UserSorts,
            schemas.UserSorts.created_at,
            sorting.SortOrders.desc,
        )
    ),
) -> pagination.Paginated[schemas.User]:
    return await query(schemas.UserListRequestSchema(pagination=pagination, sorting=sorting))


@router.get(
    "/{user_id}",
    response_model=schemas.UserDetailsFull,
)
@wiring.inject
async def get_user_details(
    user_id: UUID,
    query: UserManagementRetrieveQuery = Depends(wiring.Provide[Container.user.management_retrieve_query]),
) -> schemas.UserDetailsFull:
    return await query(user_id)


@router.patch(
    "/{user_id}",
    response_model=schemas.UserDetailsFull,
)
@wiring.inject
async def partial_update_user(
    user_id: UUID,
    payload: schemas.UserPartialUpdate,
    command: UserManagementPartialUpdateCommand = Depends(wiring.Provide[Container.user.management_update_command]),
) -> schemas.UserDetailsFull:
    return await command(user_id, schemas.UserPartialUpdateFull.model_validate(payload))


@router.post("", response_model=schemas.User)
@wiring.inject
async def create_user(
    payload: schemas.UserCredentials,
    command: UserManagementCreateCommand = Depends(wiring.Provide[Container.user.management_create_command]),
) -> schemas.UserDetails:
    return await command(payload)
