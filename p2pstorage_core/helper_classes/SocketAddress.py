from typing import NamedTuple


class SocketAddress(NamedTuple):
    host: str
    port: int
