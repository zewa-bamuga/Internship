import secrets

from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Float, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey(Role.id))

    role = relationship("Role", backref="users")
    route_ratings = relationship("RouteRating", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")


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
    user_id = Column(Integer, ForeignKey(User.id))
    survey_id = Column(Integer, ForeignKey(Survey.id))


class RouteRating(Base):
    __tablename__ = "route_rating"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    question_id = Column(Integer, ForeignKey(Question.id))
    rating = Column(Float)

    user = relationship("User", backref="route_ratings")
    question = relationship("Question")


class HistoricalEvent(Base):
    __tablename__ = "historical_events"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    event_date = Column(Date)
    event_description = Column(String)


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    text = Column(String, nullable=False)
    device_name = Column(String)
    os_version = Column(String)
    app_version = Column(String)

    user = relationship("User", backref="feedbacks")


class PasswordResetCode(Base):
    __tablename__ = "password_reset_code"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    code = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now)

    user = relationship("User")

    @classmethod
    def generate_code(cls) -> str:
        return secrets.token_urlsafe(6)


class FavoriteRoute(Base):
    __tablename__ = "favorite_route"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    question_id = Column(Integer, ForeignKey(Question.id))