from typing import NamedTuple


class SocketAddress(NamedTuple):
    host: str
    port: int

    def __str__(self) -> str:
        return f'{self.host}:{self.port}'
