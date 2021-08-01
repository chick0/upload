from configparser import ConfigParser


MegaByte = 1000 * 1000


def get() -> [int, int]:
    upload = ConfigParser()
    upload.read("upload.ini")

    max_upload = 100
    max_size = 30

    if "upload" in upload.sections():
        def fetch(option: str, fallback: int) -> int:
            try:
                return int(upload.get("upload", option, fallback=fallback))
            except ValueError:
                return fallback

        max_upload = fetch("max_upload", fallback=100)
        max_size = fetch("max_size", fallback=30)
    else:
        reset()

    return max_upload, max_size * MegaByte


def reset():
    upload = ConfigParser()
    upload.add_section("upload")
    upload.set("upload", "max_upload", "100")
    upload.set("upload", "max_size", "30")

    with open("upload.ini", mode="w", encoding="utf-8") as fp:
        upload.write(fp=fp)
        fp.write("\n".join([
            "",
            "# max_upload 옵션은 서버에 업로드 할 수 있는 파일의 개수를 제한하는 설정입니다.",
            "# - 기본값 : 100",
            "",
            "# max_size 옵션은 업로드 할 수 있는 파일의 크기를 제한합니다.",
            "# - 기본값 : 30   (단위:MB)",
        ]))
