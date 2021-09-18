from json import dumps
from os.path import join
from hashlib import md5
from hashlib import sha1
from hashlib import sha256
from secrets import token_bytes
from datetime import datetime
from datetime import timedelta

from flask import Blueprint
from flask import current_app
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import Response
from werkzeug.utils import secure_filename

from app import redis
from app import UPLOAD_DIR
from app.secret_key import SECRET_KEY
from app.custom_error import *
from app.models import File


bp = Blueprint(
    name="upload",
    import_name="upload",
    url_prefix="/",
)


def set_filename(file_id: str, filename: str) -> str:
    try:
        filename, ext = filename.rsplit(".", 1)
    except ValueError:
        filename = secure_filename(filename)
        return filename if len(filename) != 0 else file_id

    filename = secure_filename(filename)

    if len(filename) == 0:
        filename = f"{file_id}.{ext}"
    else:
        filename += f".{ext}"

    return filename


@bp.get("")
def form():
    return render_template(
        "upload/form.html",
        max_size=current_app.config['MAX_CONTENT_LENGTH']
    )


@bp.post("")
def upload():
    def check_file_id(length: int = 2) -> str:
        new_id = token_bytes(length).hex()
        if redis.exists(f"chick0/upload:{new_id}"):
            return check_file_id(length=length + 1)

        return new_id

    target = request.files.get("file", None)
    if target is None:
        raise FileIsEmpty

    file_id = check_file_id()
    blob = target.stream.read()
    size = len(blob)

    if size == 0:
        raise FileIsEmpty

    if size >= current_app.config['MAX_CONTENT_LENGTH']:
        raise FileIsTooBig

    with open(join(UPLOAD_DIR, file_id), mode="wb") as tmp_writer:
        tmp_writer.write(blob)

    file = File(
        name=set_filename(
            file_id=file_id,
            filename=target.filename
        ),
        size=size,
        md5=md5(blob).hexdigest(),
        sha1=sha1(blob).hexdigest(),
        sha256=sha256(blob).hexdigest(),
    )

    redis.set(
        name=f"chick0/upload:{file_id}",
        value=dumps(file),
        ex=2700
    )

    if "curl" in request.user_agent.string:
        return Response(
            response=f"{request.scheme}://{request.host}" + url_for("download.file", file_id=file_id),
            mimetype="text/plain"
        )

    r = redirect(url_for("file.show", file_id=file_id))
    r.set_cookie(
        key=file_id,
        value=md5(file.md5.encode() + SECRET_KEY + file_id.encode()).hexdigest(),
        expires=datetime.now() + timedelta(minutes=45),
        path=f"/file/{file_id}",
        httponly=True,
    )

    return r
