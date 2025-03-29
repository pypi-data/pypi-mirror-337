from __future__ import annotations

import pytest

from filgood.utils import extract_code_from_markdown, extract_sql_types


@pytest.mark.parametrize(
    "source, expected_result",
    [
        ("hello world **markdown**!\n\n```python\nimport xyz\n```", "import xyz"),
        (
            "hello world **markdown**!\n\n```python\nimport xyz\n\npage.hello(a, b, c, d)\npage.quit()\n```",
            "import xyz\n\npage.hello(a, b, c, d)\npage.quit()",
        ),
        (
            "hello world **markdown**!\n\n```python\nimport xyz\n\npage.hello(a, b, c, d)\npage.quit()\n"
            "```\nhello world **markdown**!",
            "import xyz\n\npage.hello(a, b, c, d)\npage.quit()",
        ),
    ],
)
def test_extract_code_from_markdown(source: str, expected_result: str) -> None:
    assert extract_code_from_markdown(source) == expected_result


@pytest.mark.parametrize(
    "source, expected_result",
    [
        (
            "-- Table definition "
            "CREATE TABLE general_fra.articles (id integer  NOT NULL,name text  NOT NULL,deleted_at timestamp without "
            "time zone ,category_id integer ,created_at timestamp without time zone DEFAULT now() NOT NULL,"
            "parent_article_id integer ,is_included boolean ,type general_fra.article_type "
            "DEFAULT 'machine'::text NOT NULL,mandatory boolean ,"
            "internal_code text  NOT NULL,meta jsonb ,billing_meta jsonb ,tenant_id integer  NOT NULL)  ",
            ["INTEGER", "TEXT", "TIMESTAMP WITHOUT TIME ZONE", "GENERAL_FRA.ARTICLE_TYPE", "BOOLEAN", "JSONB"],
        )
    ],
)
def test_extract_sql_types(source: str, expected_result: list[str]) -> None:
    for expected_type in extract_sql_types(source):
        assert expected_type in expected_result
