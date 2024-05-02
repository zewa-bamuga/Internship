import datetime
import secrets
import uuid

import sqlalchemy as sa
from sqlalchemy import orm, Column, Integer, String, ForeignKey, DateTime, Date, Float, JSON
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
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
    __tablename__ = "attachment"

    name: orm.Mapped[str]
    path: orm.Mapped[str]
    uri: orm.Mapped[str | None]


class User(Base):
    __tablename__ = "user"

    username: orm.Mapped[str] = orm.mapped_column(sa.String, unique=True)
    email: orm.Mapped[str] = orm.mapped_column(sa.String, unique=True)
    status: orm.Mapped[str]
    password_hash: orm.Mapped[str]
    avatar_attachment_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey("attachment.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    permissions: orm.Mapped[set[str] | None] = orm.mapped_column(ARRAY(sa.String))

    avatar_attachment: orm.Mapped["Attachment"] = orm.relationship(
        "Attachment",
        backref="user_avatar_attachment",
        foreign_keys=[avatar_attachment_id],
        uselist=False,
    )
    tokens: orm.Mapped[list["Token"]] = orm.relationship("Token")


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    user_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    refresh_token_id: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True))


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)


class Survey(Base):
    __tablename__ = "survey"
    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)

    questions = relationship("Question", back_populates="survey")


class Question(Base):
    __tablename__ = "question"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    short_description = Column(String)
    points = Column(Integer)
    distance = Column(Float)
    time = Column(Float)
    price = Column(Float)
    rating = Column(Float)
    image_path = Column(String)
    survey_id = Column(Integer, ForeignKey(Survey.id))

    survey = relationship("Survey", back_populates="questions")


class UserResponse(Base):
    __tablename__ = "user_response"
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id))
    survey_id = Column(Integer, ForeignKey(Survey.id))
    created_at = Column(DateTime, default=func.now, nullable=False)
    updated_at = Column(DateTime, default=func.now, onupdate=func.now, nullable=False)


class RouteRating(Base):
    __tablename__ = "route_rating"
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id))
    question_id = Column(Integer, ForeignKey(Question.id))
    rating = Column(Float)
    created_at = Column(DateTime, default=func.now, nullable=False)
    updated_at = Column(DateTime, default=func.now, onupdate=func.now, nullable=False)

    user = relationship("User", backref="route_ratings")
    question = relationship("Question")


class HistoricalEvent(Base):
    __tablename__ = "historical_event"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    event_date = Column(Date)
    event_description = Column(String)


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    text = Column(String, nullable=False)
    device_name = Column(String)
    os_version = Column(String)
    app_version = Column(String)
    created_at = Column(DateTime, default=func.now)
    updated_at = Column(DateTime, default=func.now, onupdate=func.now)

    user = relationship("User", backref="feedbacks")


class PasswordResetCode(Base):
    __tablename__ = "password_reset_code"
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    code = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now)

    user = relationship("User")

    @classmethod
    def generate_code(cls) -> str:
        return secrets.token_urlsafe(6)

    @classmethod
    def generate_code(cls) -> str:
        return secrets.token_urlsafe(6)


class FavoriteRoute(Base):
    __tablename__ = "favorite_route"
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id))
    question_id = Column(Integer, ForeignKey(Question.id))
