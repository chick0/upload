def display_size(size: int) -> str:
    if size >= 1000000:
        return f"{int(size / 1000000)} MB"
    elif size >= 1000:
        return f"{int(size / 1000)} KB"
    else:
        return f"{size} bytes"
