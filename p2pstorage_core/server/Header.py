import json
import socket
from typing import TypedDict

from p2pstorage_core.helper_classes.SocketAddress import SocketAddress
from p2pstorage_core.server.Package import PackageType, AbstractPackage, HostConnectedPackage


class HeaderDict(TypedDict):
    size: int
    type: PackageType
    from_ip: SocketAddress
    to_ip: SocketAddress


class Header:
    ENCODING_FORMAT = 'utf-8'
    MAX_SIZE = 64

    def __init__(self, size: int, package_type: PackageType, from_ip: SocketAddress, to_ip: SocketAddress):
        self.__size = size
        self.__package_type = package_type
        self.__from_ip = from_ip
        self.__to_ip = to_ip

    def get_type(self) -> PackageType:
        return self.__package_type

    def to_json(self) -> str:
        return json.dumps({
            'size': self.__size,
            'package_type': self.__package_type,
            'from_ip': self.__from_ip,
            'to_ip': self.__to_ip
        })

    def encode(self):
        return self.to_json().encode(Header.ENCODING_FORMAT).zfill(Header.MAX_SIZE)

    def __repr__(self):
        return f'Header(size={self.__size}, ' \
               f'package_type={self.__package_type}, ' \
               f'from_ip={self.__from_ip}, ' \
               f'to_ip={self.__to_ip})'

    @staticmethod
    def from_json(json_str: str) -> 'Header':
        header_dict: HeaderDict = json.loads(json_str)

        size = header_dict['size']
        package_type = header_dict['type']
        from_ip = header_dict['from_ip']
        to_ip = header_dict['to_ip']

        return Header(size, package_type, from_ip, to_ip)

    def load_package(self, client_socket: socket.socket) -> AbstractPackage:
        data = client_socket.recv(self.__size)

    @classmethod
    def decode(cls, obj: bytes) -> 'Header':
        json_str = obj.decode(Header.ENCODING_FORMAT)

        json_str = json_str[0: json_str.find('\0')]

        return cls.from_json(json_str)

    @classmethod
    def generate_from_bytes(cls, obj: bytes, package_type: PackageType,
                            from_ip: SocketAddress, to_ip: SocketAddress) -> 'Header':
        return Header(len(obj), package_type, from_ip, to_ip)
