import asyncio
import functools
from collections.abc import Callable
from typing import Any

import typer
from loguru import logger

import app.domain
from app.containers import Container
from app.domain.users.core.schemas import UserCreate, SurveyCreate, QuestionCreate
from app.domain.users.permissions.schemas import BasePermissions
from a8t_tools.db.exceptions import DatabaseError


def async_to_sync(fn: Callable[..., Any]) -> Callable[..., Any]:
    if not asyncio.iscoroutinefunction(fn):
        return fn

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        coro = fn(*args, **kwargs)
        return asyncio.get_event_loop().run_until_complete(coro)

    return wrapper


def create_container() -> Container:
    container = Container()
    container.wire(packages=[app.domain])
    container.init_resources()
    return container


container = create_container()
typer_app = typer.Typer()


@typer_app.command()
@async_to_sync
async def noop() -> None:
    pass


@typer_app.command()
@async_to_sync
async def create_superuser(
        username: str = typer.Argument(...),
        email: str = typer.Argument(...),
        password: str = typer.Argument(...),
) -> None:
    password_hash = await container.user.password_hash_service().hash(password)
    command = container.user.create_command()
    try:
        await command(
            UserCreate(
                username=username,
                email=email,
                password_hash=password_hash,
                permissions={BasePermissions.superuser},
            ),
        )
    except DatabaseError as err:
        logger.warning(f"Superuser creation error: {err}")


@typer_app.command()
@async_to_sync
async def create_survey(
        category: str = typer.Argument(...),
) -> None:
    command = container.user.create_survey()
    try:
        await command(
            SurveyCreate(
                category=category,
            ),
        )
    except DatabaseError as err:
        logger.warning(f"Survey creation error: {err}")


@typer_app.command()
@async_to_sync
async def create_question(
        title: str = typer.Argument(...),
        survey_id: int = typer.Argument(...),
        description: str = typer.Argument(...),
        short_description: str = typer.Argument(...),
        points: int = typer.Argument(...),
        distance: int = typer.Argument(...),
        time: float = typer.Argument(...),
        price: float = typer.Argument(...),
        image_path: str = typer.Argument(...),
) -> None:
    command = container.user.create_question()
    try:
        await command(
            QuestionCreate(
                title=title,
                survey_id=survey_id,
                description=description,
                short_description=short_description,
                points=points,
                distance=distance,
                time=time,
                price=price,
                image_path=image_path,
            ),
        )
    except DatabaseError as err:
        logger.warning(f"Question creation error: {err}")
