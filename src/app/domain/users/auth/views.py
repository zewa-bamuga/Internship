from typing import Union
from uuid import UUID

from dependency_injector import wiring
from fastapi import APIRouter, Body, Depends, HTTPException, Header
from pydantic import EmailStr

from app.containers import Container
from app.domain.users.auth.commands import TokenRefreshCommand, UserAuthenticateCommand
from app.domain.users.auth.schemas import TokenResponse
from app.domain.users.core import schemas
from app.domain.users.core.commands import UpdatePasswordCommand
from app.domain.users.core.queries import UserRetrieveByUsernameQuery, UserRetrieveByEmailQuery
from app.domain.users.core.schemas import UserCredentials, UpdatePassword
from app.domain.users.management.queries import UserManagementRetrieveQuery, EmailManagementRetrieveQuery
from app.domain.users.profile.views import user_token

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


@router.post(
    "/password/reset/request",
    response_model=UpdatePassword,
)
@wiring.inject
async def password_reset_request(
        email: str,
        command: UpdatePasswordCommand = Depends(wiring.Provide[Container.user.update_password_command]),
) -> UpdatePassword:
    payload = schemas.UpdatePassword(email=email)
    await command.set_user_id(email)  # Устанавливаем user_id в UpdatePasswordCommand
    try:
        return await command(payload)
    except ValueError as e:
        # Обрабатываем случай, когда пользователь не найден по электронной почте
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/get_by_username",
    response_model=UUID,
)
@wiring.inject
async def get_user_by_username(
        username: str,
        user_service: UserRetrieveByUsernameQuery = Depends(wiring.Provide[Container.user.get_user_by_username]),
) -> Union[UUID, None]:
    user = await user_service(username)
    if user:
        return user.id
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.get(
    "/{email}",
    response_model=schemas.UserDetailsFull,
)
@wiring.inject
async def get_user_by_email(
        token: str = Header(...),
        user_email: str = Header(...),
        query: EmailManagementRetrieveQuery = Depends(wiring.Provide[Container.user.management_retrieve_email_query]),
) -> schemas.UserDetailsFull:
    async with user_token(token):
        get_by_email = await query(user_email)
        return get_by_email
