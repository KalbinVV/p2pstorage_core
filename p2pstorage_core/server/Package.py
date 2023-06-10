import logging
import socket
import threading
from enum import IntEnum
import pickle
from typing import Any, Type, Self

from p2pstorage_core.helper_classes.SocketAddress import SocketAddress
from p2pstorage_core.server import StreamConfiguration
from p2pstorage_core.server.Exceptions import EmptyHeaderException
from p2pstorage_core.server.FileInfo import FileInfo, FileDataBaseInfo
from p2pstorage_core.server.Host import HostInfo


class PackageType(IntEnum):
    HOST_CONNECT_REQUEST = 1
    HOST_CONNECT_RESPONSE = 2
    CONNECTION_LOST = 3
    NEW_FILE_REQUEST = 4
    NEW_FILE_RESPONSE = 5
    HOSTS_LIST_REQUEST = 6
    HOSTS_LIST_RESPONSE = 7
    FILES_LIST_REQUEST = 8
    FILES_LIST_RESPONSE = 9
    GET_FILE_BY_ID_REQUEST = 10
    FILE_CONTAINS_REQUEST = 11
    FILE_CONTAINS_RESPONSE = 12
    FILE_TRANSACTION_START_REQUEST = 13
    FILE_TRANSACTION_START_RESPONSE = 14
    FILE_TRANSACTION_END_REQUEST = 15
    NEW_HOST_CONNECTED = 16
    TRANSACTION_FINISHED = 17


class Package:
    def __init__(self, data: Any, type_of_package: PackageType):
        self.__data = data
        self.__type = type_of_package

    def get_data(self) -> Any:
        return self.__data

    def get_type(self) -> PackageType:
        return self.__type

    def encode(self) -> bytes:
        return pickle.dumps(self)

    def send(self, host_socket: socket.socket) -> None:
        from p2pstorage_core.server.Header import Header

        logging.debug(f'Sending package to {host_socket.getpeername()}: {self}...')

        data_to_send = self.encode()

        size_of_data = len(data_to_send)

        header = Header(size_of_data)

        header.send(host_socket)
        host_socket.send(data_to_send)

    def __repr__(self) -> str:
        return f'Package(data={self.__data}, type={self.__type})'

    def __str__(self) -> str:
        return f'(data={self.__data}, type={self.__type.name})'

    @staticmethod
    def recv(host_socket: socket.socket) -> Type[Self]:
        from p2pstorage_core.server.Header import Header

        header_data = host_socket.recv(StreamConfiguration.HEADER_SIZE)

        logging.debug(f'Receiving header data from {host_socket.getpeername()}: {header_data}...')

        if not header_data:
            raise EmptyHeaderException

        header = Header.decode(header_data)

        logging.debug(f'Receive header from {host_socket.getpeername()}: {header}!')

        package = header.load_package(host_socket)

        logging.debug(f'Receive package from {host_socket.getpeername()}: {package}!')

        return package

    @staticmethod
    def decode(obj: bytes) -> Type[Self]:
        package: Self = pickle.loads(obj)

        return package


class ConnectionRequestPackage(Package):
    def __init__(self, host_name: str):
        super().__init__({
            'host_name': host_name
        }, PackageType.HOST_CONNECT_REQUEST)

    def get_host_name(self) -> str:
        return self.get_data()['host_name']

    @classmethod
    def from_abstract(cls, package: Package) -> Self:
        return cls(**package.get_data())


class ConnectionResponsePackage(Package):
    def __init__(self, connection_approved: bool = True, broadcast_message: str = '',
                 reject_reason: str = ''):
        super().__init__({
            'connection_approved': connection_approved,
            'broadcast_message': broadcast_message,
            'reject_reason': reject_reason
        }, PackageType.HOST_CONNECT_RESPONSE)

    def is_connection_approved(self) -> bool:
        return self.get_data()['connection_approved']

    def get_reason(self) -> bool:
        return self.get_data()['reject_reason']

    def get_broadcast_message(self) -> str:
        return self.get_data()['broadcast_message']

    @classmethod
    def from_abstract(cls, package: Package) -> Self:
        return cls(**package.get_data())


class ConnectionLostPackage(Package):
    def __init__(self, reason: str = '!'):
        super().__init__({
            'reason': reason
        }, PackageType.CONNECTION_LOST)

    def get_reason(self) -> str:
        return self.get_data()['reason']

    @classmethod
    def from_abstract(cls, package: Package) -> Self:
        return cls(**package.get_data())


class NewFileRequestPackage(Package):
    def __init__(self, files_info: list[FileInfo]):
        super().__init__({
            'files_info': files_info
        }, PackageType.NEW_FILE_REQUEST)

    def get_files_info(self) -> list[FileInfo]:
        return self.get_data()['files_info']

    @classmethod
    def from_abstract(cls, package: Package) -> Self:
        return cls(**package.get_data())


class NewFileResponsePackage(Package):
    def __init__(self, file_name: str = '', file_approved: bool = True, reject_reason: str = ''):
        super().__init__({
            'file_name': file_name,
            'file_approved': file_approved,
            'reject_reason': reject_reason,
        }, PackageType.NEW_FILE_RESPONSE)

    def is_file_approved(self) -> bool:
        return self.get_data()['file_approved']

    def get_reason(self) -> str:
        return self.get_data()['reject_reason']

    def get_file_name(self) -> str:
        return self.get_data()['file_name']

    @classmethod
    def from_abstract(cls, package: Package) -> Self:
        return cls(**package.get_data())


class HostsListRequestPackage(Package):
    def __init__(self):
        super().__init__({}, PackageType.HOSTS_LIST_REQUEST)


class HostsListResponsePackage(Package):
    def __init__(self, response_approved: bool = True, hosts_list: list[HostInfo] | None = None,
                 reject_reason: str = ''):
        super().__init__({
            'response_approved': response_approved,
            'hosts_list': hosts_list,
            'reject_reason': reject_reason
        }, PackageType.HOST_CONNECT_RESPONSE)

    def is_response_approved(self) -> bool:
        return self.get_data()['response_approved']

    def get_reject_reason(self) -> str:
        return self.get_data()['reject_reason']

    def get_hosts(self) -> list[HostInfo] | None:
        return self.get_data()['hosts_list']

    @classmethod
    def from_abstract(cls, package: Package) -> Self:
        return cls(**package.get_data())


class FilesListRequestPackage(Package):
    def __init__(self):
        super().__init__({}, PackageType.FILES_LIST_REQUEST)


class FilesListResponsePackage(Package):
    def __init__(self, response_approved: bool = True, files_list: list[FileDataBaseInfo] | None = None,
                 reject_reason: str = ''):
        super().__init__({
            'response_approved': response_approved,
            'files_list': files_list,
            'reject_reason': reject_reason
        }, PackageType.FILES_LIST_RESPONSE)

    def is_response_approved(self) -> bool:
        return self.get_data()['response_approved']

    def get_reject_reason(self) -> str:
        return self.get_data()['reject_reason']

    def get_files(self) -> list[FileDataBaseInfo] | None:
        return self.get_data()['files_list']

    @classmethod
    def from_abstract(cls, package: Package) -> Self:
        return cls(**package.get_data())


class GetFileByIdRequestPackage(Package):
    def __init__(self, file_id):
        super().__init__({
            'file_id': file_id
        }, PackageType.GET_FILE_BY_ID_REQUEST)

    def get_file_id(self) -> int:
        return self.get_data()['file_id']

    @classmethod
    def from_abstract(cls, package: Package) -> Self:
        return cls(**package.get_data())


class FileTransactionStartRequestPackage(Package):
    def __init__(self, file_name: str, establish_addr: SocketAddress):
        super().__init__({
            'file_name': file_name,
            'establish_addr': establish_addr
        }, PackageType.FILE_TRANSACTION_START_REQUEST)

    def get_file_name(self) -> str:
        return self.get_data()['file_name']

    def get_establish_addr(self) -> SocketAddress:
        return self.get_data()['establish_addr']

    @classmethod
    def from_abstract(cls, package: Package) -> Self:
        return cls(**package.get_data())


class FileTransactionStartResponsePackage(Package):
    def __init__(self, sender_addr: SocketAddress | None,
                 file_name: str = '',
                 transaction_started: bool = True,
                 reject_reason: str = ''):
        super().__init__({
            'sender_addr': sender_addr,
            'file_name': file_name,
            'transaction_started': transaction_started,
            'reject_reason': reject_reason
        }, PackageType.FILE_TRANSACTION_START_RESPONSE)

    def get_sender_addr(self) -> SocketAddress:
        return self.get_data()['sender_addr']

    def get_file_name(self) -> str:
        return self.get_data()['file_name']

    def is_transaction_started(self) -> bool:
        return self.get_data()['transaction_started']

    def get_reject_reason(self) -> str:
        return self.get_data()['reject_reason']

    @classmethod
    def from_abstract(cls, package: Package) -> Self:
        return cls(**package.get_data())


class FileContainsRequestPackage(Package):
    def __init__(self, file_name: str):
        super().__init__({
            'file_name': file_name
        }, PackageType.FILE_CONTAINS_REQUEST)

    def get_file_name(self) -> bool:
        return self.get_data()['file_name']

    @classmethod
    def from_abstract(cls, package: Package) -> Self:
        return cls(**package.get_data())


class FileContainsResponsePackage(Package):
    def __init__(self, file_contains: bool = True):
        super().__init__({
            'file_contains': file_contains
        }, PackageType.FILE_CONTAINS_RESPONSE)

    def is_file_contains(self) -> bool:
        return self.get_data()['file_contains']

    @classmethod
    def from_abstract(cls, package: Package) -> Self:
        return cls(**package.get_data())


class NewHostConnectedPackage(Package):
    def __init__(self, host_addr: SocketAddress, host_name: str):
        super().__init__({
            'host_addr': host_addr,
            'host_name': host_name
        }, PackageType.NEW_HOST_CONNECTED)

    def get_host_addr(self) -> SocketAddress:
        return self.get_data()['host_addr']

    def get_host_name(self) -> str:
        return self.get_data()['host_name']

    @classmethod
    def from_abstract(cls, package: Package) -> Self:
        return cls(**package.get_data())


class FileTransactionFinishedPackage(Package):
    def __init__(self, sender_addr: SocketAddress):
        super().__init__({
            'sender_addr': sender_addr
        }, PackageType.TRANSACTION_FINISHED)

    def get_sender_addr(self) -> SocketAddress:
        return self.get_data()['sender_addr']

    @classmethod
    def from_abstract(cls, package: Package) -> Self:
        return cls(**package.get_data())
