from typing import Union
from uuid import UUID

from dependency_injector import wiring
from fastapi import APIRouter, Body, Depends, HTTPException, Header, Query
from pydantic import EmailStr
from starlette.responses import JSONResponse

from app.containers import Container
from app.domain.common.models import PasswordResetCode
from app.domain.users.auth.commands import TokenRefreshCommand, UserAuthenticateCommand
from app.domain.users.auth.schemas import TokenResponse
from app.domain.users.core import schemas
from app.domain.users.core.commands import UpdatePasswordRequestCommand, UpdatePasswordConfirmCommand
from app.domain.users.core.queries import UserRetrieveByUsernameQuery, UserRetrieveByEmailQuery, UserRetrieveByCodeQuery
from app.domain.users.core.schemas import UserCredentials, UpdatePasswordRequest
# from app.domain.users.management.queries import UserManagementRetrieveQuery, EmailManagementRetrieveQuery
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
    response_model=None,
)
@wiring.inject
async def password_reset_request(
        payload: UpdatePasswordRequest,
        command: UpdatePasswordRequestCommand = Depends(wiring.Provide[Container.user.update_password_request_command]),
):
    user_details = await command(payload)
    return user_details


@router.post(
    "/password/reset/confirm",
    response_model=schemas.UpdatePasswordConfirm,
)
@wiring.inject
async def password_reset_confirm(
        payload: schemas.UpdatePasswordConfirm,
        command: UpdatePasswordConfirmCommand = Depends(wiring.Provide[Container.user.update_password_confirm_command]),
) -> schemas.UpdatePasswordConfirm:
    await command(payload)

    return payload


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
    "/get_by_email",
    response_model=UUID,
)
@wiring.inject
async def get_user_by_email(
        user_email: str = Header(...),
        query: UserRetrieveByEmailQuery = Depends(wiring.Provide[Container.user.get_user_by_email]),
) -> Union[UUID, None]:
    user_details = await query(user_email)
    return user_details.id


@router.get(
    "/get_by_code",
    response_model=UUID,
)
@wiring.inject
async def get_user_by_code(
        code: str = Header(...),
        query: UserRetrieveByCodeQuery = Depends(wiring.Provide[Container.user.get_userID_by_code]),
) -> Union[UUID, None]:
    password_reset_code = await query(code)
    return password_reset_code.user_id
