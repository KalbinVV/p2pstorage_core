from enum import IntEnum
import pickle


class PackageType(IntEnum):
    HOST_CONNECT_REQUEST = 1
    HOST_SUCCESSFUL_CONNECT_RESPONSE = 2


class Package:
    def __init__(self, data: bytes, type_of_package: PackageType):
        self.__data = data
        self.__type = type_of_package

    def get_data(self) -> bytes:
        return self.__data

    def get_type(self) -> PackageType:
        return self.__type

    def __repr__(self):
        return f'Package(data={self.__data}, type={self.__type})'

    def encode(self):
        return pickle.dumps(self)

    @staticmethod
    def decode(obj: bytes) -> 'Package':
        package: 'Package' = pickle.loads(obj)

        return package
