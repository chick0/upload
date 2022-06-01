from collections import namedtuple

File = namedtuple(
    "File",
    [
        "name",
        "size",
        "sha256",
        "code",
        "creation_date"
    ]
)

Error = namedtuple(
    "Error",
    [
        "title",
        "subtitle"
    ]
)
