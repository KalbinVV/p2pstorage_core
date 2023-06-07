from dataclasses import dataclass


@dataclass(frozen=True)
class FileInfo:
    name: str
    size: int
    hash: str
    id: int = -1
