class FileIsEmpty(Exception):
    def __init__(self):
        super().__init__()


class FileIsTooBig(Exception):
    def __init__(self):
        super().__init__()


class TooManyFiles(Exception):
    def __init__(self):
        super().__init__()


# do not touch this
__all__ = [name for name in dir() if not name.startswith("_")]
# do not touch this
