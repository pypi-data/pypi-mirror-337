from __future__ import annotations

import pytest

from filgood import ObjectType, PostgresDump


@pytest.mark.asyncio
async def test_context(connection) -> None:
    async with PostgresDump(connection) as pg_dump:
        assert pg_dump._initialized
    assert not pg_dump._initialized


@pytest.mark.asyncio
async def test_ls_table(connection) -> None:
    async with PostgresDump(connection) as pg_dump:
        tables = []

        for schema, table, priority in await pg_dump.tables():
            print(schema, table)
            assert not table.startswith("pg_")
            tables.append(table)

        assert "categories" in tables
        assert "products" in tables
        assert "users" in tables
        assert "orders" in tables
        assert "order_items" in tables
        assert "shipping" in tables
        assert "ratings" in tables


@pytest.mark.asyncio
async def test_table_priority(connection) -> None:
    async with PostgresDump(connection) as pg_dump:
        assert (await pg_dump.get_priority("public", "categories")) == 0
        assert (await pg_dump.get_priority("public", "products")) == 1
        assert (await pg_dump.get_priority("public", "users")) == 0
        assert (await pg_dump.get_priority("public", "order_items")) == 2


@pytest.mark.asyncio
async def test_dump_table(connection) -> None:
    async with PostgresDump(connection) as pg_dump:
        ddl = await pg_dump.dump(ObjectType.TABLE, "public", "categories")

        assert "CREATE TABLE public.categories" in ddl
        assert "name" in ddl
