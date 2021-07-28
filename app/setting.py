def get_max_upload() -> int:
    try:
        return int(open("max_upload.txt", mode="r", encoding="utf-8").readline())
    except (ValueError, FileNotFoundError):
        return 100


def get_size_limit() -> int:
    try:
        size = int(open("file_size_limit.txt", mode="r", encoding="utf-8").readline())
        print(size)
        print(size * 1000 * 1000)
        return size * 1000 * 1000
    except (ValueError, FileNotFoundError):
        return 30 * 1000 * 1000
