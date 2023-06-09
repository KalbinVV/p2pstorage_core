from dataclasses import dataclass


@dataclass(frozen=True)
class FileInfo:
    name: str
    size: int
    hash: str


@dataclass
class FileDataBaseInfo:
    id: int
    host_id: int
    name: str
    size: int
    hash: str

    def __init__(self, tpl: tuple[int, int, str, int, str]):
        self.id, self.host_id, self.name, self.size, self.hash = tpl

    def __str__(self) -> str:
        return f'(id={self.id}, name={self.name})'
