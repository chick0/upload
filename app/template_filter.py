from datetime import datetime
from datetime import timedelta


def display_size(size: int) -> str:
    if size >= 1000000:
        return f"{int(size / 1000000)} MB"
    elif size >= 1000:
        return f"{int(size / 1000)} KB"
    else:
        return f"{size} bytes"


def parse_timestamp(timestamp: int) -> str:
    date = datetime.fromtimestamp(timestamp)
    return date.strftime("%H시 %M분") + " ~ " + \
        (date + timedelta(minutes=45)).strftime("%H시 %M분")
