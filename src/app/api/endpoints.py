from fastapi import APIRouter, status

users_router = APIRouter(prefix="/users")

# Создайте другой роутер, который вы хотите включить в users_router
v1_router = APIRouter(prefix="/v1", tags=["users"])

# Включите v1_router в users_router
users_router.include_router(v1_router)
