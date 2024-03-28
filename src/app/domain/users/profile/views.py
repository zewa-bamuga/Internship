from dependency_injector import wiring
from fastapi import APIRouter, Depends, status

from app.containers import Container
from app.domain.users.core.schemas import UserDetails
from app.domain.users.profile import schemas
from app.domain.users.profile.commands import UserProfilePartialUpdateCommand
from app.domain.users.profile.queries import UserProfileMeQuery

router = APIRouter()


@router.get(
    "/me",
    response_model=UserDetails,
)
@wiring.inject
async def get_me(
    query: UserProfileMeQuery = Depends(wiring.Provide[Container.user.profile_me_query]),
) -> UserDetails:
    return await query()


@router.patch(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
@wiring.inject
async def update_profile(
    payload: schemas.UserProfilePartialUpdate,
    command: UserProfilePartialUpdateCommand = Depends(wiring.Provide[Container.user.profile_partial_update_command]),
) -> None:
    await command(payload)
