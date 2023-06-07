from dataclasses import dataclass


@dataclass(frozen=True)
class FileInfo:
    name: str
    size: int
    hash: str


@dataclass(frozen=True)
class FileDataBaseInfo:
    id: int
    host_id: int
    name: str
    size: int
    hash: str
