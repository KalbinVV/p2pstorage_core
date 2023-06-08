import json
import logging
import socket
from json import JSONDecodeError
from typing import TypedDict, Self, Type

from p2pstorage_core.server import StreamConfiguration
from p2pstorage_core.server.Crypt import CryptMode
from p2pstorage_core.server.Exceptions import InvalidHeaderException
from p2pstorage_core.server.Package import Package


class HeaderDict(TypedDict):
    size: int
    crypt_mode: CryptMode


class Header:
    def __init__(self, size: int, crypt_mode: CryptMode = CryptMode.UNENCRYPTED):
        self.__size = size
        self.__crypt_mode = crypt_mode

    def to_json(self) -> str:
        return json.dumps({
            'size': self.__size,
            'crypt_mode': self.__crypt_mode
        })

    def encode(self) -> bytes:
        return self.to_json().encode(StreamConfiguration.ENCODING_FORMAT)\
            .zfill(StreamConfiguration.HEADER_SIZE)

    def load_package(self, host_socket: socket.socket) -> Type[Package]:
        data = host_socket.recv(self.__size)

        return Package.decode(data)

    def send(self, host_socket: socket.socket) -> None:
        logging.debug(f'Sending header to {host_socket.getpeername()} {self}...')

        host_socket.send(self.encode())

    def __repr__(self) -> str:
        return f'Header(size={self.__size}, crypt_mode={self.__size})'

    def __str__(self) -> str:
        return self.to_json()

    @staticmethod
    def from_json(json_str: str) -> Self:
        try:
            header_dict: HeaderDict = json.loads(json_str)
        except JSONDecodeError:
            raise InvalidHeaderException

        size = header_dict['size']
        crypt_mode = header_dict['crypt_mode']

        return Header(size, crypt_mode)

    @classmethod
    def decode(cls, obj: bytes) -> Self:
        json_str = obj.decode(StreamConfiguration.ENCODING_FORMAT)

        json_str = json_str[json_str.find('{'):]

        return cls.from_json(json_str)
