from __future__ import annotations

import typing


class Definition(typing.TypedDict):
    fingerprint: str
    boilerplate: str


class CacheEntry(typing.TypedDict):
    thread: str
    definitions: dict[str, Definition]


class Cache(typing.TypedDict):
    version: str
    databases: dict[str, CacheEntry]
