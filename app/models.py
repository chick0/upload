from collections import namedtuple


File = namedtuple("File", "name size md5 sha1 sha256 code")

Error = namedtuple("Error", "title subtitle")
