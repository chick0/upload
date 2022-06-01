from collections import namedtuple

File = namedtuple(
    "File",
    [
        "name",
        "size",
        "sha256",
        "code",
    ]
)

Error = namedtuple(
    "Error",
    [
        "title",
        "subtitle"
    ]
)
