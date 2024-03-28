from dependency_injector import wiring
from fastapi import APIRouter, Depends

from app.containers import Container
from app.domain.users.core.schemas import UserCredentials, UserDetails
from app.domain.users.registration.commands import UserRegisterCommand

router = APIRouter()


@router.post(
    "/registration",
    response_model=UserDetails,
)
@wiring.inject
async def register(
    payload: UserCredentials,
    command: UserRegisterCommand = Depends(wiring.Provide[Container.user.register_command]),
) -> UserDetails:
    return await command(payload)
