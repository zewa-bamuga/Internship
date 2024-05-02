from dependency_injector import wiring
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.containers import Container
from app.domain.users.auth.commands import TokenRefreshCommand, UserAuthenticateCommand
from app.domain.users.auth.schemas import TokenResponse
from app.domain.users.core.schemas import UserCredentials

router = APIRouter()


@router.post(
    "/authentication",
    response_model=TokenResponse,
)
@wiring.inject
async def authenticate(
    payload: UserCredentials,
    command: UserAuthenticateCommand = Depends(wiring.Provide[Container.user.authenticate_command]),
) -> TokenResponse:
    return await command(payload)


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
@wiring.inject
async def update_refresh_token(
        refresh_token: str = Body(embed=True),
        command: TokenRefreshCommand = Depends(wiring.Provide[Container.user.refresh_token_command]),
) -> TokenResponse:
    return await command(refresh_token)
