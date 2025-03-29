from __future__ import annotations

import typing
from os import environ
from pathlib import Path

import aiofile
import asyncpg
import pytest_asyncio

from filgood import DatabaseFaker

CURRENT_DIRECTORY = Path(__file__).parent


@pytest_asyncio.fixture(scope="session", autouse=True)
async def use_fixture() -> typing.AsyncGenerator[None]:
    conn: asyncpg.Connection = await asyncpg.connect(environ.get("POSTGRES_DSN"))

    async with aiofile.async_open(CURRENT_DIRECTORY.joinpath("fixture.sql"), "r") as fp:
        await conn.execute(await fp.read())

    yield

    await conn.execute("DROP TABLE order_items CASCADE")
    await conn.execute("DROP TABLE shipping CASCADE")
    await conn.execute("DROP TABLE ratings CASCADE")
    await conn.execute("DROP TABLE orders CASCADE")
    await conn.execute("DROP TABLE products CASCADE")
    await conn.execute("DROP TABLE categories CASCADE")
    await conn.execute("DROP TABLE users CASCADE")

    await conn.close()


@pytest_asyncio.fixture(scope="function")
async def connection() -> typing.AsyncGenerator[asyncpg.Connection]:
    conn: asyncpg.Connection = await asyncpg.connect(environ.get("POSTGRES_DSN"))

    yield conn

    await conn.close()


@pytest_asyncio.fixture(scope="function")
async def pg_faker() -> typing.AsyncGenerator[DatabaseFaker]:
    async with DatabaseFaker(environ.get("POSTGRES_DSN")) as db_faker:
        yield db_faker
