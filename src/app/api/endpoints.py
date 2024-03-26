from fastapi import APIRouter, status



users_router = APIRouter(prefix="/users")
users_router.include_router(
    prefix="/v1",
    tags=["users"],
)