from os import path
from os import mkdir
from os import environ
from secrets import token_bytes

from flask import g
from flask import Flask
from flask import Response
from flask_redis import FlaskRedis
from dotenv import load_dotenv

redis = FlaskRedis()
BASE_DIR = path.dirname(path.abspath(__file__))
UPLOAD_DIR = path.join(BASE_DIR, "upload")


def upload_path_test():
    if not path.isdir(UPLOAD_DIR):
        mkdir(UPLOAD_DIR)


def get_secret_key() -> bytes:
    try:
        with open(".SECRET_KEY", mode="rb") as key_reader:
            key = key_reader.read()
    except FileNotFoundError:
        with open(".SECRET_KEY", mode="wb") as key_writer:
            key = token_bytes(32)
            key_writer.write(key)

    return key


def create_app():
    load_dotenv()
    upload_path_test()

    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = int(environ['MAX_SIZE']) * 1000 * 1000
    app.config['REDIS_URL'] = environ['REDIS_URL']
    app.config['SECRET_KEY'] = get_secret_key()

    # redis init
    redis.init_app(app=app)

    # blueprint init
    from app import views
    for view in views.__all__:
        app.register_blueprint(getattr(getattr(views, view), "bp"))

    # filter init
    from app import template_filter
    for x in [x for x in [getattr(template_filter, x) for x in dir(template_filter) if not x.startswith("_")] if x.__class__.__name__ == "function"]:
        app.add_template_filter(x)

    # register error handler
    from .error import error_map
    for code in error_map:
        app.register_error_handler(code, error_map[code])

    @app.before_request
    def set_title():
        g.title = "업로드"

    @app.get("/robots.txt")
    def txt():
        return Response(
            response="\n".join([
                "User-agent: *",
                "Allow: /$",
                "Allow: /static",
                "Disallow: /",
            ]),
            mimetype="text/plain"
        )

    return app
