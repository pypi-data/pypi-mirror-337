from __future__ import annotations

import os

import pytest

from filgood import GrowthStrategy


@pytest.mark.asyncio
@pytest.mark.skipif("OPENAI_API_KEY" not in os.environ, reason="Test requires OpenAI API key")
async def test_stats_empty(pg_faker) -> None:
    table_count = 0

    async for table, row_count in pg_faker.stats():
        assert row_count == 0
        table_count += 1

    assert table_count


@pytest.mark.asyncio
@pytest.mark.skipif("OPENAI_API_KEY" not in os.environ, reason="Test requires OpenAI API key")
async def test_fill_database_flat_increase(pg_faker) -> None:
    await pg_faker.load(
        strategy=GrowthStrategy.BY_ROW_COUNT,
        increase=32,
        ignore_empty_table=False,
    )

    table_count = 0

    async for table, row_count in pg_faker.stats():
        assert row_count == 32
        table_count += 1

    assert table_count
