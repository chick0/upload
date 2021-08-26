from os import path
from os import mkdir
from os import remove
from os import listdir

from flask import g
from flask import Flask
from flask import request
from flask_redis import FlaskRedis

from .config import get
from .template_filter import display_size


redis = FlaskRedis()
BASE_DIR = path.dirname(path.abspath(__file__))
UPLOAD_DIR = path.join(BASE_DIR, "upload")


def upload_path_test():
    if not path.isdir(UPLOAD_DIR):
        mkdir(UPLOAD_DIR)


def create_app():
    upload_path_test()
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'],\
        app.config['REDIS_URL'] = get()

    # redis init
    redis.init_app(app=app)

    # blueprint init
    from . import views
    for view in views.__all__:
        app.register_blueprint(getattr(getattr(getattr(__import__(f"app.views.{view}"), "views"), view), "bp"))

    # filter init
    app.add_template_filter(display_size)

    # register error handler
    from .error import error_map
    for code in error_map:
        app.register_error_handler(code, error_map[code])

    @app.before_request
    def set_title():
        g.title = "Upload!"

    @app.teardown_request
    def chick0_upload_queue(exception):
        if request.path.startswith("/file"):
            if not redis.exists("chick0/upload/queue"):
                for file_id in listdir(UPLOAD_DIR):
                    if not redis.exists(f"chick0/upload:{file_id}"):
                        remove(path.join(UPLOAD_DIR, file_id))

                # 5min
                redis.set("chick0/upload/queue", "", ex=300)

    return app
