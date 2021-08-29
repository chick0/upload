from os import path
from os import remove
from os import listdir
from sys import exit
from time import time
from time import sleep
from logging import INFO
from logging import getLogger
from logging import Formatter
from logging import StreamHandler
from configparser import ConfigParser

from redis import StrictRedis

BASE_DIR = path.dirname(path.abspath(__file__))
UPLOAD_DIR = path.join(BASE_DIR, "app", "upload")


def worker():
    logger = getLogger()

    logger.info("staring worker...")
    config = ConfigParser()
    config.read("upload.ini")

    logger.info("connecting to redis server...")
    redis = StrictRedis.from_url(url=config['upload']['redis_url'])

    while True:
        logger.info("starting task")
        start_time = time()

        for file_id in listdir(UPLOAD_DIR):
            if not redis.exists(f"chick0/upload:{file_id}"):
                try:
                    remove(path.join(UPLOAD_DIR, file_id))
                except (OSError, Exception):
                    logger.exception(f"fail to remove '{file_id}'")

        logger.info(f"task finished ({round(time() - start_time, 2)}s)")
        sleep(90)  # 1min 30s


if __name__ == "__main__":
    def logger_init():
        logger = getLogger()
        logger.setLevel(INFO)

        fmt = Formatter("%(asctime)s [%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S")
        sh = StreamHandler()
        sh.setFormatter(fmt)

        logger.addHandler(sh)

    try:
        logger_init()
        worker()
    except KeyboardInterrupt:
        exit(0)
