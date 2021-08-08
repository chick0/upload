from argparse import ArgumentParser
from logging import getLogger
from logging import FileHandler

from waitress import serve
from paste.translogger import TransLogger

from app import create_app


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--port", metavar="PORT", help="포트번호 설정", action="store", type=int, default=16482)
    args = parser.parse_args()

    logger = getLogger("wsgi")
    logger.addHandler(hdlr=FileHandler("wsgi.log"))
    serve(TransLogger(create_app(), setup_console_handler=False), port=args.port, _quiet=True)
