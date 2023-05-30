import socket

from p2pstorage_core.helper_classes.SocketAddress import SocketAddress
from p2pstorage_core.server.Header import Header
from p2pstorage_core.server.Package import AbstractPackage
from p2pstorage_core.server.PackageHandler import AbstractPackageHandler


class StorageServer:
    def __init__(self, package_handler: AbstractPackageHandler, socket_address: SocketAddress):
        self.__package_handler = package_handler
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.bind(socket_address)

        running = True

        pass

    def handle_connection(self, client_socket: socket.socket) -> None:
        connection_active = True

        while connection_active:
            header_data = client_socket.recv(Header.MAX_SIZE)

            header = Header.decode(header_data)

            package: AbstractPackage = header.load_package(client_socket)

            self.__package_handler.handle_package(package)
