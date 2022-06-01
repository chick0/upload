from os import path
from os import mkdir
from os import environ

from flask import g
from flask import Flask
from flask_redis import FlaskRedis
from dotenv import load_dotenv

from app.template_filter import display_size


redis = FlaskRedis()
BASE_DIR = path.dirname(path.abspath(__file__))
UPLOAD_DIR = path.join(BASE_DIR, "upload")


def upload_path_test():
    if not path.isdir(UPLOAD_DIR):
        mkdir(UPLOAD_DIR)


def create_app():
    load_dotenv()
    upload_path_test()

    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = int(environ['MAX_SIZE']) * 1000 * 1000
    app.config['REDIS_URL'] = environ['REDIS_URL']

    # redis init
    redis.init_app(app=app)

    # blueprint init
    from app import views
    for view in views.__all__:
        app.register_blueprint(getattr(getattr(views, view), "bp"))

    # filter init
    app.add_template_filter(display_size)

    # register error handler
    from .error import error_map
    for code in error_map:
        app.register_error_handler(code, error_map[code])

    @app.before_request
    def set_title():
        g.title = "업로드"

    return app
