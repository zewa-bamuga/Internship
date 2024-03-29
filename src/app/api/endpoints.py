from fastapi import APIRouter, status

import app.domain.storage.attachments.views
import app.domain.users.auth.views
import app.domain.users.management.views
import app.domain.users.profile.views
import app.domain.users.registration.views
from app.api import schemas

users_router = APIRouter(prefix="/users")
users_router.include_router(
    app.domain.users.profile.views.router,
    prefix="/v1",
    tags=["users"],
)
users_router.include_router(
    app.domain.users.auth.views.router,
    prefix="/v1",
    tags=["users"],
)
users_router.include_router(
    app.domain.users.registration.views.router,
    prefix="/v1",
    tags=["users"],
)
users_router.include_router(
    app.domain.users.management.views.router,
    prefix="/v1",
    tags=["users"],
)

storage_router = APIRouter(prefix="/storage")
storage_router.include_router(
    app.domain.storage.attachments.views.router,
    prefix="/v1/attachments",
    tags=["attachments"],
)

router = APIRouter(
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": schemas.AuthApiError},
        status.HTTP_403_FORBIDDEN: {"model": schemas.SimpleApiError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.SimpleApiError},
    }
)


router.include_router(users_router)
router.include_router(storage_router)
