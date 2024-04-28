import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.sql import func


@orm.as_declarative()
class Base:
    __tablename__: str

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(sa.DateTime(timezone=True), server_default=func.now())
    updated_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Attachment(Base):
    __tablename__ = "attachments"

    name: orm.Mapped[str]
    path: orm.Mapped[str]
    uri: orm.Mapped[str | None]


class User(Base):
    __tablename__ = "user"

    username: orm.Mapped[str] = orm.mapped_column(sa.String, unique=True)
    status: orm.Mapped[str]
    password_hash: orm.Mapped[str]
    avatar_attachment_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey("attachments.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    permissions: orm.Mapped[set[str] | None] = orm.mapped_column(ARRAY(sa.String))

    avatar_attachment: orm.Mapped["Attachment"] = orm.relationship(
        "Attachment",
        backref="user_avatar_attachments",
        foreign_keys=[avatar_attachment_id],
        uselist=False,
    )
    tokens: orm.Mapped[list["Token"]] = orm.relationship("Token")


class Token(Base):
    __tablename__ = "tokens"

    user_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    refresh_token_id: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True))
