import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, String
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
import enum

from database.db import Base

user_id_pk_fk = Annotated[int, mapped_column(ForeignKey("users.id"), primary_key=True)]
id_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
varchar_50 = Annotated[str, mapped_column(String(50))]
varchar_100 = Annotated[str, mapped_column(String(100))]
varchar_200 = Annotated[str, mapped_column(String(200))]


class Roles(enum.Enum):
    admin = "admin"
    user = "user"


class UsersModel(Base):
    __tablename__ = "users"
    id: Mapped[id_pk]
    username: Mapped[varchar_50]
    email: Mapped[varchar_100]
    password_hash: Mapped[varchar_100]
    role: Mapped[Roles]
    git_credentials: Mapped[str | None]  # GIT authorization data (json)
    github_url: Mapped[str | None]
    sign_up_date: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    last_login_date: Mapped[datetime.datetime]
    is_active: Mapped[bool]  # Active or not active (banned) account.


class ProjectModel(Base):
    __tablename__ = "projects"
    id: Mapped[id_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[varchar_50]
    creation_date: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    local_path: Mapped[str]  # local path to project
    repository_url: Mapped[str]
    config_file_path: Mapped[str]  # local path to project config file
    license_type: Mapped[varchar_50]  # GNU, MIT, etc.
    is_public: Mapped[bool]


class LicenseModel(Base):
    __tablename__ = "licenses"
    id: Mapped[id_pk]
    title: Mapped[varchar_50]
    description: Mapped[str]


class RepositoryTemplatesModel(Base):
    __tablename__ = "repository_templates"
    id: Mapped[id_pk]
    title: Mapped[varchar_50]
    source_url: Mapped[str | None]  # .GIT or local path


class DocumentationModel(Base):
    __tablename__ = "documentation"
    id: Mapped[id_pk]
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    type: Mapped[str]  # open-source or legal
    content: Mapped[str]


class UserSettingsModel(Base):
    __tablename__ = "user_settings"
    user_id: Mapped[user_id_pk_fk]
    settings: Mapped[str]  # json with settings
