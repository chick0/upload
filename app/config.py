from configparser import ConfigParser


MegaByte = 1000 * 1000


def get() -> (int, str):
    upload = ConfigParser()
    upload.read("upload.ini", encoding="utf-8")

    max_size = 30
    redis_url = "redis://:@localhost:6379/0"

    if "upload" in upload.sections():
        def fetch(option: str, fallback: int) -> int:
            try:
                return int(upload.get("upload", option, fallback=fallback))
            except ValueError:
                return fallback

        max_size = fetch("max_size", fallback=30)
        redis_url = upload.get("upload", "redis_url", fallback=redis_url)
    else:
        reset()

    return max_size * MegaByte, redis_url


def reset():
    upload = ConfigParser()
    upload.add_section("upload")
    upload.set("upload", "max_size", "30")
    upload.set("upload", "redis_url", "redis://:@localhost:6379/0")

    with open("upload.ini", mode="w", encoding="utf-8") as fp:
        upload.write(fp=fp)
        fp.write("\n".join([
            "",
            "#",
            "# max_size 옵션은 업로드 할 수 있는 파일의 크기를 제한합니다.",
            "# - 기본값 : 30   (단위:MB)",
            "#",
            "# redis_url 옵션은 파일정보를 저장하는 Redis 서버 접속 정보를 설정합니다.",
            "# - 기본값 : redis://:@localhost:6379/0",
            "#",
        ]))
