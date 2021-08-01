from time import time
from time import sleep
from threading import Thread

from flask import Flask
from asgiref.wsgi import WsgiToAsgi

from .config import get
from .template_filter import display_size


storage = {}


def loop():
    while True:
        for key in list(storage.keys()):
            alive = 2700 - round(time() - storage[key]['time'])
            if alive < 0:
                del storage[key]

        # 5m
        sleep(5 * 60)


def create_app():
    app = Flask(__name__)
    app.config['MAX_UPLOAD'], \
        app.config['MAX_CONTENT_LENGTH'] = get()

    # blueprint init
    from . import views
    for view in views.__all__:
        app.register_blueprint(getattr(getattr(getattr(__import__(f"app.views.{view}"), "views"), view), "bp"))

    # filter init
    app.add_template_filter(display_size)

    # background task
    Thread(target=loop, daemon=True).start()

    # register error handler
    from .error import error_map
    for code in error_map:
        app.register_error_handler(code, error_map[code])

    return WsgiToAsgi(app)
