from time import time
from time import sleep
from threading import Thread

from flask import Flask
from flask import render_template
from asgiref.wsgi import WsgiToAsgi

from .setting import get_size_limit
from .setting import get_max_upload
from .template_filter import display_size


storage = {}


def loop():
    while True:
        for key in list(storage.keys()):
            alive = 2700 - int(time() - storage[key]['time'])
            if alive < 0:
                del storage[key]

        sleep(30)


def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = get_size_limit()
    app.config['MAX_UPLOAD'] = get_max_upload()

    # blueprint init
    from . import views
    for view in views.__all__:
        app.register_blueprint(getattr(getattr(getattr(__import__(f"app.views.{view}"), "views"), view), "bp"))

    # filter init
    app.add_template_filter(display_size)

    # background task
    task = Thread(target=loop)
    task.daemon = True
    task.start()

    # error page!
    def error_413(err):
        return render_template(
            "upload/file_is_too_big.html"
        ), 413

    app.register_error_handler(413, error_413)
    return WsgiToAsgi(app)
