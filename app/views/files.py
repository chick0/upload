from json import loads

from flask import Blueprint
from flask import session
from flask import render_template

from app import redis
from app.tuples import File

bp = Blueprint("files", __name__, url_prefix="/files")


@bp.get("")
def show_all():
    files = []
    file_id_storage = {}
    for file_id in session.keys():
        t = redis.get(f"chick0/upload:{file_id}")
        if t is not None:
            file = File(*loads(t))
            if file.code == session[file_id]:
                files.append(file)
                file_id_storage[file.code] = file_id

    return render_template(
        "files/show_all.html",
        files=files,
        file_id_storage=file_id_storage
    )
