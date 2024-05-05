import logging
from dataclasses import dataclass
from typing import Any, Dict, Literal, Tuple, TypeVar, Union

from core.settings import PostgresSettings
from sqlalchemy import (
    DATETIME,
    TIMESTAMP,
    Delete,
    MetaData,
    Result,
    Select,
    select,
    TextClause,
    UpdateBase,
    ValuesBase,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID, insert
from sqlalchemy.dialects.postgresql.dml import Insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm.decl_api import (
    DeclarativeAttributeIntercept,
    MappedAsDataclass,
)

Query = Union[ValuesBase, Select, UpdateBase, Delete, Insert]
Model = TypeVar("Model", bound=DeclarativeAttributeIntercept)
Field_table = Tuple[str, int]
Field_names = str
Sorted_direction = Literal["ASC", "DESC"]
Sorted_order = Dict[Field_names, Sorted_direction]


@dataclass
class Base(MappedAsDataclass, DeclarativeBase):
    """Setting up metadata.

    In particular, we specify a schema for storing tables.
    """

    metadata = MetaData(
        schema=PostgresSettings().postgres_schema,
        quote_schema=True,
    )
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    created: Mapped[DATETIME] = mapped_column(
        TIMESTAMP,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
    modified: Mapped[DATETIME] = mapped_column(
        TIMESTAMP,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        init=False,
    )

    def __repr__(self):
        """Redefinition.

        Returns:
            object: new instance name
        """
        return "{class_name}(id={id})".format(
            id=self.id,
            class_name=self.__class__.__name__,
        )

    __str__ = __repr__


class PostgresAccessor:
    """Description of the rules for connecting.

    PostgresSQL to the Fast-Api application.
    """

    def __init__(self, logger=logging.getLogger(__name__)):
        self.settings = PostgresSettings()
        self._db = Base
        self._engine = create_async_engine(
            self.settings.dsn(True),
            echo=False,
            future=True,
        )
        self.logger = logger

    async def disconnect(self):
        """Closing the connection to the database."""
        if self._engine:
            await self._engine.dispose()
        self.logger.info(f"{self.__class__.__name__} disconnected")

    @property
    def session(self) -> AsyncSession:
        """Get the async session for the database.

        Returns:
            AsyncSession: the async session for the database
        """
        return AsyncSession(self._engine, expire_on_commit=False)

    @staticmethod
    def get_query_insert(model: Model, **insert_data) -> Query:
        """Get query inserted.

        Args:
            model: Table model
            insert_data: fields for insert dict[name, value]

        Returns:
        object: query
        """
        return insert(model).values(**insert_data)

    async def query_execute(self, query: Union[Query, TextClause]) -> Result[Any]:
        """Query execute.

        Args:
            query: CRUD query for Database

        Returns:
              Any: result of query
        """
        async with self.session.begin().session as session:
            result = await session.execute(query)
            await session.commit()
            return result

    async def query_executes(self, *query: Query) -> list[Result[Any]]:
        """Query executes.

        Args:
            query: CRUD query for Database

        Returns:
              Any: result of query
        """
        async with self.session as session:
            result = [await session.execute(q) for q in query]
            await session.commit()
            return result

    @staticmethod
    def get_query_select_by_field(
            model: Model, field_name: str, field_value: Any
    ) -> Query:
        """Get a query by field name.

        Args:
            model: Table model
            field_name: Field names in the model
            field_value: Field values in the model

        Returns:
            object: Query object
        """
        return select(model).where(
            text(f"{model.__tablename__}.{field_name} = '{field_value}'")
        )
