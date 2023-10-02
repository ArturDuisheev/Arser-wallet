from core import settings

class BaseDataException(Exception):
    error_data = {
    }

    def __init__(self, error: str):
        self.error_data[settings.default_error_key] = error
        super().__init__(error)


class CodeDataException(BaseDataException):

    def __init__(self, error, status=400):
        self.status = status
        super().__init__(error)