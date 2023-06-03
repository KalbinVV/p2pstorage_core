class EmptyHeaderException(Exception):
    def __init__(self, msg: str = 'Header data is empty!'):
        super().__init__(msg)


class InvalidHeaderException(Exception):
    def __init__(self, msg: str = 'Invalid header!'):
        super().__init__(msg)
