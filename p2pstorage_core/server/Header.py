import json
import logging
import socket
from json import JSONDecodeError
from typing import TypedDict

from p2pstorage_core.server import StreamConfiguration
from p2pstorage_core.server.Exceptions import InvalidHeaderException
from p2pstorage_core.server.Package import Package


class HeaderDict(TypedDict):
    size: int


class Header:
    def __init__(self, size: int):
        self.__size = size

    def to_json(self) -> str:
        return json.dumps({
            'size': self.__size
        })

    def encode(self) -> bytes:
        return self.to_json().encode(StreamConfiguration.ENCODING_FORMAT)\
            .zfill(StreamConfiguration.HEADER_SIZE)

    def load_package(self, host_socket: socket.socket) -> 'Package':
        data = host_socket.recv(self.__size)

        return Package.decode(data)

    def send(self, host_socket: socket.socket) -> None:
        logging.debug(f'Sending header {self}...')

        host_socket.send(self.encode())

    def __repr__(self) -> str:
        return f'Header(size={self.__size}'

    @staticmethod
    def from_json(json_str: str) -> 'Header':
        try:
            header_dict: HeaderDict = json.loads(json_str)
        except JSONDecodeError:
            raise InvalidHeaderException

        size = header_dict['size']

        return Header(size)

    @classmethod
    def decode(cls, obj: bytes) -> 'Header':
        json_str = obj.decode(StreamConfiguration.ENCODING_FORMAT)

        json_str = json_str[json_str.find('{'):]

        return cls.from_json(json_str)
