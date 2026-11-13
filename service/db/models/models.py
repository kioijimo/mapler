from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class Cog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Action(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cog_id: int | None = Field(default=None, foreign_key="cog.id")
    name: str
    description: str
    modified_at: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Guild(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    modified_at: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ActionGreeting(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    action_id: int | None = Field(default=None, foreign_key="action.id")
    guild_id: int | None = Field(default=None, foreign_key="guild.id")
    msg: str | None = None
    embed: str | None = None
    channel: int | None = None
    role: int | None = None
    trigger: str | None = None
    modified_at: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
