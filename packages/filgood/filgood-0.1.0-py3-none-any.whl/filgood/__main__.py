from __future__ import annotations

import argparse
import asyncio
from os import environ
from pathlib import Path
from sys import argv

from rich.console import Console
from rich.progress import Progress, TaskID
from rich.prompt import Prompt
from rich.table import Table

from ._version import version
from .core import DatabaseFaker, GrowthStrategy, context_debug

DEFAULT_CACHE_PATH = str(Path.home().joinpath(".filgood.cache"))


async def cli() -> None:
    parser = argparse.ArgumentParser(prog="smartfaker", description="LLM agent for filling a database with fake records")

    parser.add_argument(
        "database",
        help="Postgres database DSN to be used",
    )

    parser.add_argument(
        "-i",
        action="store",
        default="100%",
        dest="increase",
        help="Percentage increase or flat row count target for data injection",
    )

    parser.add_argument(
        "-s",
        "--schema",
        action="store",
        default=None,
        dest="schema",
        help="Target a specific schema",
    )

    parser.add_argument(
        "-t",
        "--table",
        action="store",
        default=None,
        dest="table",
        help="Target a specific table",
    )

    parser.add_argument(
        "--no-cache",
        action="store_true",
        default=False,
        dest="cache_disabled",
        help="Disable the cache (LLM)",
    )

    parser.add_argument(
        "--skip-empty",
        action="store_true",
        default=False,
        dest="skip_empty",
        help="Skip empty table",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        dest="verbose",
        help="Enable advanced debugging",
    )

    args = parser.parse_args(argv[1:])

    print(
        rf"""
   _____                      _   ______    _
  / ____|      {version}        | | |  ____|  | |
 | (___  _ __ ___   __ _ _ __| |_| |__ __ _| | _____ _ __
  \___ \| '_ ` _ \ / _` | '__| __|  __/ _` | |/ / _ \ '__|
  ____) | | | | | | (_| | |  | |_| | | (_| |   <  __/ |
 |_____/|_| |_| |_|\__,_|_|   \__|_|  \__,_|_|\_\___|_|
"""
    )

    print("!> Welcome to the playground")
    print("!> This will help you to quickly fill a database", end="\n\n")

    if "OPENAI_API_KEY" not in environ:
        openai_key = Prompt.ask("(Warning) Provide OpenAI API Key: ", password=True)

        if not openai_key:
            exit(1)
    else:
        openai_key = None

    console = Console()

    focus_table: str | None = args.table
    focus_schema: str | None = args.schema

    debug_enabled = args.verbose is True
    cache_disabled = args.cache_disabled is True
    skip_empty = args.skip_empty is True

    target_size = args.increase

    strategy = GrowthStrategy.BY_PERCENT_INCREASE if target_size.endswith("%") else GrowthStrategy.BY_ROW_COUNT

    if target_size.endswith("%"):
        target_size = target_size[:-1]

    try:
        target_size = int(target_size)
    except ValueError:
        print(f"> {target_size} is not a valid parameter for size increase. either set '300' or '300%' for example.")
        exit(1)

    if target_size <= 0:
        print(f"> {target_size} must be greater than 0")
        exit(1)

    ctx_debug = context_debug()

    if debug_enabled:
        ctx_debug.__enter__()

    async with DatabaseFaker(
        args.database,
        cache_path=DEFAULT_CACHE_PATH if cache_disabled is False else None,
        openai_key=openai_key,
    ) as db_faker:
        assert db_faker._pg_dump is not None

        table = Table(title="Database Overview")

        table.add_column("Schema", justify="right", style="cyan", no_wrap=True)
        table.add_column("Table", style="magenta")
        table.add_column("Depth / Layer", justify="right", style="green")
        table.add_column("Row Count", justify="right", style="green")

        async for current_schema_table, row_count in db_faker.stats(schema=focus_schema):
            listed_schema, listed_table = current_schema_table.split(".", maxsplit=1)

            if focus_table is not None and listed_table != focus_table:
                continue

            table.add_row(
                listed_schema,
                listed_table,
                str(await db_faker._pg_dump.get_priority(listed_schema, listed_table)),
                str(row_count),
            )

        console.print(table)

        with Progress() as progress:
            progress_matrix: dict[str, TaskID] = {}

            def _inner_task_watch(s, t, failure_count, success_count, total):
                progress_key = f"{s}.{t}"

                if f"{s}.{t}" not in progress_matrix:
                    progress_matrix[progress_key] = progress.add_task(f"[cyan]{progress_key}", total=total)

                progress.update(progress_matrix[progress_key], completed=failure_count + success_count)

            await db_faker.load(
                target_schema=focus_schema,
                target_table=focus_table,
                strategy=strategy,
                callback_progress=_inner_task_watch if not debug_enabled else None,
                increase=target_size,
                ignore_empty_table=skip_empty,
            )

    if debug_enabled:
        ctx_debug.__exit__(None, None, None)

    exit(0)


def boot() -> None:
    asyncio.run(cli())


if __name__ == "__main__":
    boot()
