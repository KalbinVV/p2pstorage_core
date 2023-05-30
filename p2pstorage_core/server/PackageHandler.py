from p2pstorage_core.server.Package import AbstractPackage


class AbstractPackageHandler:
    def handle_package(self, package: AbstractPackage) -> None:
        raise Exception('Method should be overriden!')
