import uuid
from typing import List
from uuid import UUID

from a8t_tools.db.pagination import PaginationCallable, Paginated
from a8t_tools.db.sorting import SortingData
from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.db.utils import CrudRepositoryMixin
from pydantic import BaseModel
from sqlalchemy import ColumnElement, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from app.domain.common import models, enums
from app.domain.common.schemas import IdContainer, IdContainerTables
from app.domain.users.core import schemas


class SurveyRepository(CrudRepositoryMixin[models.Survey]):

    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.Survey
        self.transaction = transaction

    async def create_survey(self, payload: schemas.SurveyCreate) -> IdContainerTables:
        return IdContainerTables(id=await self._create(payload))

    async def create_user_response(self, payload: schemas.UserСhoiceSurvey) -> IdContainerTables:
        return IdContainerTables(id=await self._create(payload))

    async def get_surveys(
            self,
            pagination: PaginationCallable[schemas.Survey] | None = None,
            sorting: SortingData[schemas.SurveySorts] | None = None,
    ) -> Paginated[schemas.Survey]:
        return await self._get_list(
            schemas.Survey,
            pagination=pagination,
            sorting=sorting,
        )


class QuestionRepository(CrudRepositoryMixin[models.Question]):

    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.Question
        self.transaction = transaction

    async def create_question(self, payload: schemas.QuestionCreate) -> IdContainerTables:
        return IdContainerTables(id=await self._create(payload))


class UpdatePasswordRepository(CrudRepositoryMixin[models.PasswordResetCode]):

    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.PasswordResetCode
        self.transaction = transaction

    async def create_update_password(self, payload: schemas.PasswordResetCode) -> IdContainerTables:
        return IdContainerTables(id=await self._create(payload))

    async def get_password_reset_code_by_code_or_none(self,
                                                      where: schemas.PasswordResetCodeWhere) -> schemas.PasswordResetCode | None:
        return await self._get_or_none(
            schemas.PasswordResetCode,
            condition=await self._format_filters_code(where),
        )

    async def _format_filters_code(self, where: schemas.PasswordResetCodeWhere) -> ColumnElement[bool]:
        filters: list[ColumnElement[bool]] = []

        if where.id is not None:
            filters.append(models.PasswordResetCode.id == where.id)

        if where.code is not None:
            filters.append(models.PasswordResetCode.code == where.code)

        return and_(*filters)


class UserRepository(CrudRepositoryMixin[models.User]):
    load_options: list[ExecutableOption] = [
        selectinload(models.User.avatar_attachment),
    ]

    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.User
        self.transaction = transaction

    async def get_users(
            self,
            pagination: PaginationCallable[schemas.User] | None = None,
            sorting: SortingData[schemas.UserSorts] | None = None,
    ) -> Paginated[schemas.User]:
        return await self._get_list(
            schemas.User,
            pagination=pagination,
            sorting=sorting,
            options=self.load_options,
        )

    async def get_user_by_filter_or_none(self, where: schemas.UserWhere) -> schemas.UserInternal | None:
        return await self._get_or_none(
            schemas.UserInternal,
            condition=await self._format_filters(where),
            options=self.load_options,
        )

    async def get_user_by_filter_by_email_or_none(self, where: schemas.UserWhere) -> schemas.UserInternal | None:
        return await self._get_or_none(
            schemas.UserInternal,
            condition=await self._format_filters_email(where),
            options=self.load_options,
        )

    async def create_user(self, payload: schemas.UserCreate) -> IdContainer:
        return IdContainer(id=await self._create(payload))

    async def partial_update_user(self, user_id: UUID, payload: schemas.UserPartialUpdate) -> None:
        return await self._partial_update(user_id, payload)

    async def delete_user(self, user_id: UUID) -> None:
        return await self._delete(user_id)

    async def set_user_status(self, user_id: UUID, status: enums.UserStatuses) -> None:
        return await self._partial_update(user_id, schemas.UserPartialUpdate(status=status))

    async def _format_filters(self, where: schemas.UserWhere) -> ColumnElement[bool]:
        filters: list[ColumnElement[bool]] = []

        if where.id is not None:
            filters.append(models.User.id == where.id)

        if where.username is not None:
            filters.append(models.User.username == where.username)

        return and_(*filters)

    async def _format_filters_email(self, where: schemas.UserWhere) -> ColumnElement[bool]:
        filters: list[ColumnElement[bool]] = []

        if where.id is not None:
            filters.append(models.User.id == where.id)

        if where.email is not None:
            filters.append(models.User.email == where.email)

        return and_(*filters)
