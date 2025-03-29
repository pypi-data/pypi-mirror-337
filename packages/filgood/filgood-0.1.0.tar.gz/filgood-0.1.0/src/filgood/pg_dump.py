from __future__ import annotations

from asyncio import Semaphore
from collections import deque
from enum import StrEnum

from asyncpg import Connection, PostgresError, Record  # type: ignore[import-untyped]

from .constants import DB_LEVEL_ANALYSIS, DBMS_METADATA
from .exceptions import SmartFakerError


class ObjectType(StrEnum):
    """Type of Postgres that we can target for DDL generation."""

    TABLE = "TABLE"
    TYPE = "TYPE"
    PROCEDURE = "PROCEDURE"
    DOMAIN = "DOMAIN"


class PostgresDump:
    """A very light and minimal pg_dump implementation in pure Python and SQL.

    The main usage of this class is to be able to get a basic
    understanding of the tables in various schemas."""

    def __init__(self, connection: Connection, excluded_schemas: list[str] | None = None) -> None:
        self._connection = connection
        self._setup = Semaphore()
        self._excluded_schemas = excluded_schemas or []
        self._initialized: bool = False

    async def install(self) -> None:
        """Execute SQL pre-requisites needed to be able to inspect the database."""
        if self._initialized:
            return

        async with self._setup:
            try:
                await self._connection.execute("CREATE SCHEMA dbms_metadata")
            except PostgresError:
                self._initialized = True
                return

            try:
                await self._connection.execute(DBMS_METADATA)
                await self._connection.execute(DB_LEVEL_ANALYSIS)
            except PostgresError as e:
                raise Exception(
                    "Unable to setup our native dump utils into your database. Do you have sufficient privilege?"
                ) from e

            self._initialized = True

    async def uninstall(self) -> None:
        """Remove previously set SQL pre-requisites. Everything was stored in the `dbms_metadata` schema."""
        if not self._initialized:
            return

        async with self._setup:
            try:
                await self._connection.execute("DROP SCHEMA dbms_metadata CASCADE")
            except PostgresError:
                return

            self._initialized = False

    async def __aenter__(self) -> PostgresDump:
        await self.install()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.uninstall()

    async def dump(self, object_type: ObjectType, schema: str, name: str) -> str:
        """Choose to get a basic DDL for any of 'TABLE', 'TYPE', 'PROCEDURE' or 'DOMAIN'."""
        if not self._initialized:
            await self.install()

        dump: Record | None = await self._connection.fetchrow(
            "SELECT dbms_metadata.get_ddl($1, $2, $3)",
            object_type.value,
            name,
            schema,
        )

        if dump is None:
            raise SmartFakerError(f"unable to dump {object_type} for {schema}.{name}")

        return dump.get("get_ddl")

    @property
    async def schemas(self) -> list[str]:
        """List of available schemas (that your db user can see)"""
        if not self._initialized:
            await self.install()

        records: list[Record] = await self._connection.fetch(
            "SELECT DISTINCT schema_name FROM dbms_metadata.dependencies ORDER BY schema_name ASC",
        )

        return [record.get("schema_name") for record in records if record.get("schema_name") not in self._excluded_schemas]

    async def tables(self, schema: str | None = None) -> deque[tuple[str, str, int]]:
        """Retrieve a list of tables ordered by layers.
        Each layer depends on the lower level excepted for the layer 0."""
        queue: deque[tuple[str, str, int]] = deque()

        if schema is None:
            records: list[Record] = await self._connection.fetch(
                "SELECT schema_name, table_name, dependency_depth "
                "FROM dbms_metadata.dependencies ORDER BY schema_name, dependency_depth DESC",
            )
        else:
            records = await self._connection.fetch(
                "SELECT schema_name, table_name, dependency_depth "
                "FROM dbms_metadata.dependencies ORDER BY dependency_depth DESC",
            )

        for record in records:
            if record.get("schema_name") not in self._excluded_schemas:
                queue.appendleft((record.get("schema_name"), record.get("table_name"), record.get("dependency_depth")))

        return queue

    async def get_priority(self, schema: str, table: str) -> int:
        """Immediately retrieve the layer on which the target table is."""
        if not self._initialized:
            await self.install()

        dump: Record | None = await self._connection.fetchrow(
            "SELECT dependency_depth FROM dbms_metadata.dependencies WHERE schema_name = $1 AND table_name = $2",
            schema,
            table,
        )

        if dump is None:
            raise SmartFakerError(f"unable to determine priority for table {schema}.{table}")

        return dump.get("dependency_depth")
