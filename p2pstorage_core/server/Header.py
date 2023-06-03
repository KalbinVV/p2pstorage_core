import json
import socket
from typing import TypedDict

from p2pstorage_core.helper_classes.SocketAddress import SocketAddress
from p2pstorage_core.server import StreamConfiguration
from p2pstorage_core.server.Package import Package


class HeaderDict(TypedDict):
    size: int
    from_ip: SocketAddress


class Header:
    def __init__(self, size: int, from_ip: SocketAddress):
        self.__size = size
        self.__from_ip = from_ip

    def to_json(self) -> str:
        return json.dumps({
            'size': self.__size,
            'from_ip': tuple(self.__from_ip)
        })

    def encode(self) -> bytes:
        return self.to_json().encode(StreamConfiguration.ENCODING_FORMAT)\
            .zfill(StreamConfiguration.HEADER_SIZE)

    def load_package(self, host_socket: socket.socket) -> 'Package':
        data = host_socket.recv(self.__size)

        return Package.decode(data)

    def send(self, host_socket: socket.socket) -> None:
        host_socket.send(self.encode())

    def __repr__(self) -> str:
        return f'Header(size={self.__size}, ' \
               f'from_ip={self.__from_ip}'

    @staticmethod
    def from_json(json_str: str) -> 'Header':
        header_dict: HeaderDict = json.loads(json_str)

        size = header_dict['size']
        from_ip = header_dict['from_ip']

        return Header(size, from_ip)

    @classmethod
    def decode(cls, obj: bytes) -> 'Header':
        json_str = obj.decode(StreamConfiguration.ENCODING_FORMAT)

        json_str = json_str[json_str.find('{'):]

        return cls.from_json(json_str)
