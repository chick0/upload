from io import BytesIO
from json import loads
from os.path import join

from flask import Blueprint
from flask import abort
from flask import send_file

from app import redis
from app import UPLOAD_DIR
from app.tuples import File

bp = Blueprint("download", __name__, url_prefix="/download")


@bp.get("/<string:file_id>")
@bp.get("/<string:file_id>/<string:fake>")
def file(file_id: str, fake=None):
    from_redis = redis.get(f"chick0/upload:{file_id}")
    if from_redis is None:
        return abort(404)

    from_redis = loads(from_redis)
    file_ = File(*from_redis)

    try:
        with open(join(UPLOAD_DIR, file_id), mode="rb") as tmp_reader:
            blob = tmp_reader.read()
    except FileNotFoundError:
        return abort(404)

    return send_file(
        BytesIO(blob),
        mimetype="application/octet-stream",
        as_attachment=True,
        attachment_filename=file_.name
    )
