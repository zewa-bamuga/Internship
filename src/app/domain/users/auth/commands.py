import json
import uuid
from typing import Any

from a8t_tools.security import tokens

from src.app.domain.users.auth.repositories import TokenRepository
from src.app.domain.users.auth.schemas import TokenResponse, TokenInfo, TokenPayload
from src.app.domain.users.core.schemas import UserInternal


class TokenCreateCommand:
    def __init__(
            self,
            repository: TokenRepository,
            jwt_service: tokens.JwtServiceBase,
    ) -> None:
        self.repository = repository
        self.jwt_service = jwt_service

    async def __call__(self, user: UserInternal) -> TokenResponse:
        token_id = uuid.uuid4()
        await self.repository.create_token_info(TokenInfo(user_id=user.id, token_id=token_id))

        return await self._get_token_data(user, token_id)

    async def _get_token_data(self, user: UserInternal, token_id: uuid.UUID) -> TokenResponse:
        access_token = await self.jwt_service.encode(await self._format_access_token_payload(user), "access")
        refresh_token = await self.jwt_service.encode(await self._format_refresh_token_payload(token_id), "refresh")

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def _format_access_token_payload(self, user: UserInternal) -> Any:
        return json.loads(TokenPayload(sub=user.id).model_dump_json())

    async def _format_refresh_token_payload(self, token_id: uuid.UUID) -> Any:
        return json.loads(TokenPayload(sub=token_id).model_dump_json())


class TokenRefreshCommand:
    def __init__(
            self,
            repository: TokenRepository,
            query: TokenPayloadQuery,
            command: TokenCreateCommand,
            user_query: UserRetrieveQuery,
    ) -> None:
        self.repository = repository
        self.query = query
        self.command = command
        self.user_query = user_query
