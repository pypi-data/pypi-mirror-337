from __future__ import annotations

import re
from hashlib import sha256


def extract_code_from_markdown(source: str, language: str = "python") -> str:
    """Retrieve the content of a source code embedded in a Markdown document."""
    match = re.search(rf"```{language.lower()}\n(.*?)\n```", source, re.DOTALL)

    if not match:
        raise ValueError(f"{language.capitalize()} code snippet not found in source")

    return re.sub(r'(["\']#.*?["\'])', lambda e: f"'{re.sub(r'(?<!\\):', r'\\:', e.group(1).strip('\'"'))}'", match.group(1))


def extract_sql_types(sql_statement: str):
    """Extracts a list of unique data types from a raw SQL statement."""
    start = sql_statement.find("(") + 1
    end = None

    open_parenthesis = 1

    for idx, c in zip(range(start, len(sql_statement[start:])), sql_statement[start:]):
        if c == "(":
            open_parenthesis += 1
            continue
        if c == ")":
            open_parenthesis -= 1

        if open_parenthesis == 0:
            end = idx
            break

    table_definition = sql_statement[start:end].strip()

    columns = []

    accumulator = ""
    in_parenthesis = 0

    for c in table_definition:
        if c == "," and not in_parenthesis:
            columns.append(accumulator.strip())
            accumulator = ""
            continue
        if c == "(":
            in_parenthesis += 1
        elif c == ")":
            in_parenthesis -= 1

        accumulator += c

    if accumulator:
        columns.append(accumulator)

    unique_types = set()

    for column in columns:
        instructions = column.strip().split()
        word_count = len(instructions)

        if word_count > 1:
            possible_type = instructions[1].upper()

            if len(instructions) > 2:
                if possible_type == "TIMESTAMP":
                    possible_specifier = instructions[2].upper()

                    if possible_specifier in {"WITH", "WITHOUT"}:
                        possible_type = f"{possible_type} {possible_specifier} TIME ZONE"
                elif possible_type == "CHARACTER":
                    possible_specifier = instructions[2].upper()

                    if possible_specifier.startswith("VARYING"):
                        possible_type = f"{possible_type} {possible_specifier}"

            if possible_type.endswith(")"):
                remove_trailing_parenthesis = False

                if possible_type.count(")") == 2:
                    remove_trailing_parenthesis = True
                elif "(" not in possible_type:
                    remove_trailing_parenthesis = True

                if remove_trailing_parenthesis:
                    possible_type = possible_type[:-1]

            unique_types.add(possible_type)

    return list(unique_types)


def fingerprint(source: str) -> str:
    """Basic sha256 applied to a Unicode string."""
    return sha256(source.encode(), usedforsecurity=False).hexdigest()
