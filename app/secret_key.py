from secrets import token_bytes

SECRET_KEY = token_bytes(32)

try:
    with open(".SECRET_KEY", mode="rb") as key_reader:
        SECRET_KEY = key_reader.read()
except FileNotFoundError:
    with open(".SECRET_KEY", mode="wb") as key_writer:
        key_writer.write(SECRET_KEY)
