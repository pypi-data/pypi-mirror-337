from __future__ import annotations

import asyncio
import json
import logging
import typing
from contextlib import contextmanager
from enum import IntEnum

# the import MUST remain as-is. The codegen expect "asyncpg" in globals.
import asyncpg  # type: ignore[import-untyped]
from aiofile import async_open
from openai import AsyncOpenAI
from openai.types.beta import Assistant, Thread
from openai.types.beta.threads import TextContentBlock

from ._version import version
from .constants import DEFAULT_AGENT_NAME, DEFAULT_CACHE_PATH, WORLD_PROMPT
from .exceptions import SmartFakerError
from .pg_dump import ObjectType, PostgresDump
from .structures import Cache, CacheEntry, Definition
from .utils import extract_code_from_markdown, extract_sql_types, fingerprint

logger = logging.getLogger(__name__)


@contextmanager
def context_debug() -> typing.Generator[None]:  # Defensive: debugging purpose only
    old_level = logger.level
    logger.setLevel(logging.DEBUG)
    explain_handler = logging.StreamHandler()
    explain_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(explain_handler)
    try:
        yield
    finally:
        logger.setLevel(old_level)
        logger.removeHandler(explain_handler)


class GrowthStrategy(IntEnum):
    BY_ROW_COUNT = 0
    BY_PERCENT_INCREASE = 1


class DatabaseFaker:
    """All-in-one utility to spawn random data in a Postgres database."""

    def __init__(
        self,
        database_dsn: str,
        database_pool_size: int = 32,
        cache_path: str | None = DEFAULT_CACHE_PATH,
        agent_name: str = DEFAULT_AGENT_NAME,
        *,
        excluded_schemas: list[str] | None = None,
        openai_key: str | None = None,
        openai_organization: str | None = None,
        openai_project: str | None = None,
        openai_model: str = "gpt-4o",
    ) -> None:
        """
        :param database_dsn: A valid DSN to connect to your target Postgres database
        :param cache_path: The file path used to store the cache
        :param agent_name: A unique and reusable agent name
        :param excluded_schemas: A list of schemas to exclude from analysis and generation
        :param openai_key: Your openai API key
        :param openai_organization: (optional) organization id to be used (openai)
        :param openai_project: (optional) project id to be used (openai)
        :param openai_model: (gpt-4o by default) model to use (openai)
        """
        self._database_dsn: str = database_dsn
        self._database_pool_size: int = database_pool_size

        self._openai = AsyncOpenAI(
            api_key=openai_key,
            organization=openai_organization,
            project=openai_project,
        )
        self._openai_model = openai_model

        self._cache_path: str | None = cache_path
        self._agent_name: str = f"{agent_name}.{version}"

        self._connection: asyncpg.Connection | None = None
        self._pool: asyncpg.Pool | None = None

        self._pg_dump: PostgresDump | None = None

        self._agent: Assistant | None = None
        self._thread: Thread | None = None

        self._cache: Cache | None = None

        self._excluded_schemas = excluded_schemas or []

    async def __aenter__(self) -> DatabaseFaker:
        if self._cache_path is not None:
            try:
                async with async_open(self._cache_path, "r") as fp:
                    self._cache = json.loads(await fp.read())
                logger.debug(f"existing cache loaded from {self._cache_path}")
            except FileNotFoundError:  # we purposely don't use os.path.exist to exclusively rely on the async i/o backend
                logger.debug(
                    f"cache file not found {self._cache_path}"
                )  # Defensive: the file may legitimately not exist if first run.

        if self._cache is None and self._cache_path is not None:
            logger.debug("initializing a fresh cache object")
            self._cache = Cache(
                version=version,
                databases={},
            )
        elif self._cache is not None:
            if version != self._cache["version"]:
                logger.warning("cache was generated from an outdated version. invalidating the whole thing now.")
                self._cache = Cache(
                    version=version,
                    databases={},
                )

        db_key = fingerprint(self._database_dsn)

        self._pool = await asyncpg.create_pool(self._database_dsn, min_size=1, max_size=self._database_pool_size)
        self._connection = await self._pool.acquire()

        try:
            logger.debug(f"connected to postgres {self._connection._addr} version {self._connection._server_version}")
        except AttributeError:  # in case of asyncpg internal changes
            logger.warning("connected to postgres (unknown info)")

        self._pg_dump = PostgresDump(self._connection)

        await self._pg_dump.install()
        logger.debug("light postgres dump utilities are installed (into dbms_metadata schema)")

        agent: Assistant | None = None

        async for assistant in self._openai.beta.assistants.list():
            if assistant.name == self._agent_name:
                agent = assistant
                logger.debug(f"AI assistant {self._agent_name} found")
                break

        if agent is None:
            logger.debug(f"AI assistant {self._agent_name} not found")
            agent = await self._openai.beta.assistants.create(
                model=self._openai_model,
                name=self._agent_name,
                instructions=WORLD_PROMPT,
            )

        self._agent = agent

        assert self._cache is not None

        if self._cache_path is None or db_key not in self._cache["databases"]:
            logger.debug(f"Database ID '{db_key}' never seen before. Creating a new thread for it.")
            self._thread = await self._openai.beta.threads.create()

            if self._cache is not None:
                self._cache["databases"][db_key] = CacheEntry(thread=self._thread.id, definitions={})
        else:
            thread_id = self._cache["databases"][db_key]["thread"]

            logger.debug(f"Database ID '{db_key}' already seen. Retrieving thread '{thread_id}'.")

            self._thread = await self._openai.beta.threads.retrieve(thread_id)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._cache_path is not None and self._cache is not None:
            logger.debug(f"Persisting cache into {self._cache_path}")

            async with async_open(self._cache_path, "w") as fp:
                await fp.write(json.dumps(self._cache, indent=2))

        assert self._pg_dump is not None

        await self._pg_dump.uninstall()
        logger.debug("Removing utilities for Postgres. Schema dbms_metadata should no longer be present.")

        assert self._pool is not None

        await self._pool.release(self._connection)
        await self._pool.close()

        logger.debug("Connection to Postgres closed. Goodbye.")

    async def _prompt(self, order: str) -> str:
        """Throw a specific prompt to the current thread and wait for the LLM answer eagerly."""
        short_debug_prompt: str = order.replace("\n", "\\n")[:100]

        logger.debug(f"Sending a prompt to the LLM assistant: '{short_debug_prompt}...'")

        assert self._thread is not None
        assert self._agent is not None

        await self._openai.beta.threads.messages.create(
            thread_id=self._thread.id,
            role="user",
            content=order,
        )

        run = await self._openai.beta.threads.runs.create_and_poll(
            thread_id=self._thread.id,
            assistant_id=self._agent.id,
        )

        if run.status != "completed":
            raise SmartFakerError("OpenAI LLM failed to provide an answer to prompt via agent")

        logger.debug(f"Retrieving the response for: '{short_debug_prompt}...'")

        messages = await self._openai.beta.threads.messages.list(thread_id=self._thread.id)

        message = await anext(messages.__aiter__())

        response = ""

        for block in message.content:
            if isinstance(block, TextContentBlock):
                response += block.text.value

        return response

    async def _learn(
        self,
        focus_schema: str | None = None,
        focus_table: str | None = None,
        ignore_empty_table: bool = True,
    ) -> typing.AsyncIterator[tuple[str, str, int, int, typing.Callable[[asyncpg.Connection], typing.Awaitable[str | None]]]]:
        """Make sure every bit of knowledge about the database is up-to-date.
        Then output necessary tools to populate the database."""
        db_key: str = fingerprint(self._database_dsn)
        target_layer: int | None = None

        assert self._pg_dump is not None
        assert self._connection is not None
        assert self._cache is not None

        if focus_schema and focus_table:
            target_layer = await self._pg_dump.get_priority(focus_schema, focus_table)
            logger.debug(f"for {focus_schema}.{focus_table} we are targeting layer n°{target_layer}")

        logger.debug("Starting the database in-depth analysis for each table in each schemas")

        for schema, table, priority in await self._pg_dump.tables(schema=focus_schema):
            table_key: str = f"{schema}.{table}"

            if focus_table is not None and table != focus_table:
                if target_layer is None:
                    continue
                elif priority >= target_layer:
                    continue

            logger.debug(f"analysing {table_key} with {priority=}")

            record: asyncpg.Record | None = await self._connection.fetchrow(
                f"SELECT COUNT(*) as row_count FROM {schema}.{table}"
            )

            if record is None:
                continue

            row_count: int = record.get("row_count")

            logger.debug(f"{table_key} has current {row_count} record(s)")

            if ignore_empty_table and not row_count:
                logger.debug(f"ignoring {table_key} because its empty.")
                continue

            if self._excluded_schemas is not None and schema in self._excluded_schemas:
                logger.debug(f"{schema} schema is excluded from analysis skipping")
                continue

            table_ddl = await self._pg_dump.dump(ObjectType.TABLE, schema, table)
            logger.debug(f"{table_key} dump: {table_ddl.replace('\n', ' ')}")

            used_types = extract_sql_types(table_ddl)
            logger.debug(f"{table_key} types: {used_types}")

            types_ddl = []

            while used_types:
                cleared_types = []
                new_types = []

                for used_type in used_types:
                    if "." in used_type:
                        host_schema, type_name = used_type.split(".", maxsplit=1)

                        try:
                            types_ddl.append(await self._pg_dump.dump(ObjectType.TYPE, host_schema.lower(), type_name.lower()))
                            logger.debug(f"{table_key} dumped type definition for: {used_type}")

                            for dependent_type in extract_sql_types(types_ddl[-1]):
                                if dependent_type in cleared_types or dependent_type in used_types:
                                    continue

                                logger.debug(f"{table_key} discovered type: {dependent_type}")
                                new_types.append(dependent_type)
                        except asyncpg.RaiseError:
                            # we don't really know in advance if it's about a real
                            # custom type or "domain" aka. constraint shortcuts.
                            types_ddl.append(
                                await self._pg_dump.dump(ObjectType.DOMAIN, host_schema.lower(), type_name.lower())
                            )
                            logger.debug(f"{table_key} dumped domain (aka. constraint) definition for: {used_type}")

                    cleared_types.append(used_type)

                for cleared_type in cleared_types:
                    used_types.remove(cleared_type)

                for new_type in new_types:
                    used_types.append(new_type)

            if types_ddl:
                types_ddl = sorted(types_ddl)

                full_ddl = f"""-- Type definitions
{"\n".join(types_ddl)}

{table_ddl}"""
            else:
                full_ddl = table_ddl

            if types_ddl:
                logger.debug(f"Found additional context types for {table_key}: {types_ddl}")

            prompt_template: str = f"""Here is the SQL schema for the table `{table}` within `{schema}` schema.

```sql
{full_ddl}
```
"""

            prompt_fingerprint: str = fingerprint(prompt_template)
            definition: Definition | None = None

            llm_uptodate: bool = False

            if self._cache_path is not None and table_key in self._cache["databases"][db_key]["definitions"]:
                definition = self._cache["databases"][db_key]["definitions"][table_key]

                if prompt_fingerprint == definition["fingerprint"]:
                    logger.debug(f"cache hit for {table_key}")
                    llm_uptodate = True
                else:
                    logger.debug(
                        f"cache outdated for {table_key} | current({prompt_fingerprint}) vs old({definition['fingerprint']})"
                    )
                    definition["fingerprint"] = prompt_fingerprint
            else:
                logger.debug(f"cache miss for {table_key}")
                definition = Definition(
                    fingerprint=prompt_fingerprint,
                    boilerplate="",
                )

            if not llm_uptodate:
                await self._prompt(prompt_template)

                codegen_response: str = await self._prompt(
                    f"Generate the Python script for the `{table}` table within `{schema}` schema."
                )

                definition["boilerplate"] = codegen_response
            else:
                codegen_response = definition["boilerplate"]

            if self._cache_path is not None:
                self._cache["databases"][db_key]["definitions"][table_key] = definition

            python_code: str = extract_code_from_markdown(codegen_response)

            logger.debug(f"attempt to dynamically load coroutine for {table_key}")

            # the most dangerous part of the program. we can't guaranty anything.
            # I don't like it either. Just look the other way.
            exec(python_code)

            # if everything went fine, the async function "insert" will be stored here.
            generate_function_hot_load = locals()["insert"]

            logger.debug(f"{table_key} coroutine loaded: {generate_function_hot_load}")

            yield schema, table, priority, row_count, generate_function_hot_load

    async def _fix_attempt(
        self, schema: str, table: str, intelligible_error: str
    ) -> typing.Callable[[asyncpg.Connection], typing.Awaitable[str | None]]:
        db_key: str = fingerprint(self._database_dsn)
        table_key = f"{schema}.{table}"

        assert self._cache is not None

        iter_learn = await self._prompt(
            f"The Python code for {table} table within {schema} did not work. An error occurred: {intelligible_error}. "
            "Did you forget to take into account constraints or types? Generate it again."
        )

        if self._cache_path is not None and table_key in self._cache["databases"][db_key]["definitions"]:
            definition: Definition = self._cache["databases"][db_key]["definitions"][table_key]
            definition["boilerplate"] = iter_learn

        python_code: str = extract_code_from_markdown(iter_learn)

        logger.debug(f"attempt to dynamically load coroutine for {table_key}")

        # the most dangerous part of the program. we can't guaranty anything.
        # I don't like it either. Just look the other way.
        exec(python_code)

        # if everything went fine, the async function "insert" will be stored here.
        generate_function_hot_load = locals()["insert"]

        logger.debug(f"{table_key} coroutine loaded: {generate_function_hot_load}")

        return generate_function_hot_load

    async def stats(self, schema: str | None = None) -> typing.AsyncIterator[tuple[str, int]]:
        """Get an overview of your database for statistic purposes."""
        assert self._pg_dump is not None
        assert self._connection is not None

        for schema, table, priority in await self._pg_dump.tables(schema=schema):
            if schema in self._excluded_schemas:
                continue

            record: asyncpg.Record | None = await self._connection.fetchrow(
                f"SELECT COUNT(*) as row_count FROM {schema}.{table}"
            )

            if record is None:
                yield f"{schema}.{table}", 0
            else:
                yield f"{schema}.{table}", record.get("row_count")

    async def load(
        self,
        target_schema: str | None = None,
        target_table: str | None = None,
        strategy: GrowthStrategy = GrowthStrategy.BY_PERCENT_INCREASE,
        increase: int = 300,
        ignore_empty_table: bool = True,
        codegen_retries: int | None = 5,
        callback_progress: typing.Callable[[str, str, int, int, int], None] | None = None,
    ) -> None:
        """Start a task to fill the database with fake entries.

        Be careful with your parameters. You may inadvertently cripple your storage or worst, your containers or OS.
        SmartFaker does not watch for the remaining free storage space.

        You have two available strategies:
        A) Percentage based increase based on existing records size (recommended)
        B) Flat increase everywhere by row count (not recommended)

        By default, the strategy is 300% increase.

        This ignores every empty table by default. Set ignore_empty_table=False to undo this.
        """

        async def _insert_with_acquire_conn(_inner_coroutine) -> str | None:
            assert self._pool is not None
            async with self._pool.acquire() as conn:
                return await _inner_coroutine(conn)

        async for schema, table, priority, row_count, insert in self._learn(
            focus_schema=target_schema,
            focus_table=target_table,
            ignore_empty_table=ignore_empty_table,
        ):
            if ignore_empty_table and not row_count:
                continue
            elif not ignore_empty_table and not row_count and strategy is GrowthStrategy.BY_PERCENT_INCREASE:
                row_count = 1

            if target_table is not None and table != target_table and row_count >= 100:
                continue

            required_task_count: int

            if strategy is GrowthStrategy.BY_PERCENT_INCREASE:
                required_task_count = round(row_count * (increase / 100))
            else:
                required_task_count = increase

            if required_task_count == 0:
                logger.debug(f"insignificant rows for {schema}.{table} (skipping)")
                continue

            # learning curve[...]
            logger.debug(f"verifying working state of dynamic Python code for {schema}.{table}")

            try:
                any_error = await insert(self._connection)
            except (
                Exception
            ) as e:  # we don't really have a choice. it's that broad because we need to catch things like AttributeError!
                any_error = str(e)

            error_count: int = 0

            while any_error is not None and codegen_retries is not None:
                error_count += 1

                logger.warning(
                    f"The LLM sold us an unusable version of the codegen. Attempting to fix it. Attempt n°{error_count}"
                )

                if error_count >= codegen_retries:
                    logger.error(f"The LLM was completely unable to generate a proper code for {schema}.{table}. Sorry.")
                    break

                insert = await self._fix_attempt(schema, table, any_error)

                try:
                    any_error = await insert(self._connection)
                except Exception as e:
                    any_error = str(e)

                if any_error is None:
                    logger.debug("The LLM seems to have fixed the issue.")

            if codegen_retries is not None and error_count >= codegen_retries and any_error is not None:
                continue

            tasks = [_insert_with_acquire_conn(insert) for _ in range(required_task_count - 1)]

            logger.debug(f"spawning {required_task_count} task(s) for {schema}.{table}")

            error_count = 0
            success_count = 1

            for completed_task in asyncio.as_completed(tasks):
                res = await completed_task

                if res is None:
                    success_count += 1
                else:
                    error_count += 1

                if callback_progress is not None:
                    callback_progress(schema, table, error_count, success_count, len(tasks) + 1)

            logger.debug(f"{schema}.{table} has been filled")
