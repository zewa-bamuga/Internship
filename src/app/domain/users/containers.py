from dependency_injector import containers, providers
from passlib.context import CryptContext

from app.domain.users.auth.commands import (
    TokenCreateCommand,
    TokenRefreshCommand,
    UserAuthenticateCommand,
)
from app.domain.users.auth.queries import (
    CurrentUserQuery,
    CurrentUserTokenPayloadQuery,
    CurrentUserTokenQuery,
    TokenPayloadQuery,
)
from app.domain.users.management.queries import (
    UserManagementListQuery,
    UserManagementRetrieveQuery,
)
from app.domain.users.auth.repositories import TokenRepository
from app.domain.users.core.commands import (
    UserActivateCommand,
    UserCreateCommand,
    UserPartialUpdateCommand,
)
from app.domain.users.core.queries import (
    UserListQuery,
    UserRetrieveByUsernameQuery,
    UserRetrieveQuery,
)
from app.domain.users.core.repositories import UserRepository
from app.domain.users.permissions.queries import UserPermissionListQuery
from app.domain.users.permissions.services import UserPermissionService
from app.domain.users.registration.commands import UserRegisterCommand
from app.domain.users.profile.queries import UserProfileMeQuery
from app.domain.users.profile.commands import UserProfilePartialUpdateCommand
from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.security.hashing import PasswordHashService
from a8t_tools.security.tokens import JwtHmacService, JwtRsaService, token_ctx_var


class UserContainer(containers.DeclarativeContainer):
    transaction = providers.Dependency(instance_of=AsyncDbTransaction)

    secret_key = providers.Dependency(instance_of=str)

    private_key = providers.Dependency(instance_of=str)

    public_key = providers.Dependency(instance_of=str)

    pwd_context = providers.Dependency(instance_of=CryptContext)

    access_expiration_time = providers.Dependency(instance_of=int)

    refresh_expiration_time = providers.Dependency(instance_of=int)

    repository = providers.Factory(
        UserRepository,
        transaction=transaction,
    )

    list_query = providers.Factory(
        UserListQuery,
        repository=repository,
    )

    retrieve_query = providers.Factory(
        UserRetrieveQuery,
        repository=repository,
    )

    retrieve_by_username_query = providers.Factory(
        UserRetrieveByUsernameQuery,
        repository=repository,
    )

    create_command = providers.Factory(
        UserCreateCommand,
        repository=repository,
    )

    activate_command = providers.Factory(
        UserActivateCommand,
        repository=repository,
    )

    password_hash_service = providers.Factory(
        PasswordHashService,
        pwd_context=pwd_context,
    )

    jwt_rsa_service = providers.Factory(
        JwtRsaService,
        private_key=private_key,
        public_key=public_key,
        access_expiration_time=access_expiration_time,
        refresh_expiration_time=refresh_expiration_time,
    )

    jwt_hmac_service = providers.Factory(
        JwtHmacService,
        secret_key=secret_key,
        access_expiration_time=access_expiration_time,
        refresh_expiration_time=refresh_expiration_time,
    )

    partial_update_command = providers.Factory(
        UserPartialUpdateCommand,
        repository=repository,
    )

    token_ctx_var_object = providers.Object(token_ctx_var)

    current_user_token_query = providers.Factory(
        CurrentUserTokenQuery,
        token_ctx_var=token_ctx_var_object,
    )

    permission_list_query = providers.Factory(
        UserPermissionListQuery,
        query=retrieve_query,
    )

    register_command = providers.Factory(
        UserRegisterCommand,
        user_create_command=create_command,
        password_hash_service=password_hash_service,
    )

    token_repository = providers.Factory(TokenRepository, transaction=transaction)

    token_create_command = providers.Factory(
        TokenCreateCommand,
        jwt_service=jwt_rsa_service,
        repository=token_repository,
    )

    token_payload_query = providers.Factory(
        TokenPayloadQuery,
        jwt_service=jwt_rsa_service,
    )

    current_user_token_payload_query = providers.Factory(
        CurrentUserTokenPayloadQuery,
        token_query=current_user_token_query,
        token_payload_query=token_payload_query,
    )

    permission_service = providers.Factory(
        UserPermissionService,
        query=permission_list_query,
        current_user_token_payload_query=current_user_token_payload_query,
    )

    current_user_query = providers.Factory(
        CurrentUserQuery,
        token_query=current_user_token_payload_query,
        user_query=retrieve_query,
    )

    authenticate_command = providers.Factory(
        UserAuthenticateCommand,
        user_retrieve_by_username_query=retrieve_by_username_query,
        password_hash_service=password_hash_service,
        command=token_create_command,
    )

    refresh_token_command = providers.Factory(
        TokenRefreshCommand,
        repository=token_repository,
        query=token_payload_query,
        command=token_create_command,
        user_query=retrieve_query,
    )

    management_list_query = providers.Factory(
        UserManagementListQuery,
        permission_service=permission_service,
        query=list_query,
    )

    profile_me_query = providers.Factory(
        UserProfileMeQuery,
        permission_service=permission_service,
        current_user_query=current_user_query,
    )

    profile_partial_update_command = providers.Factory(
        UserProfilePartialUpdateCommand,
        permission_service=permission_service,
        current_user_query=current_user_query,
        user_partial_update_command=partial_update_command,
    )