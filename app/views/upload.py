from json import dumps
from os.path import join
from hashlib import md5
from hashlib import sha1
from hashlib import sha256
from secrets import token_bytes

from flask import Blueprint
from flask import current_app
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from werkzeug.utils import secure_filename

from app import redis
from app import UPLOAD_DIR
from app.custom_error import *
from app.models import File


bp = Blueprint(
    name="upload",
    import_name="upload",
    url_prefix="/",
)


@bp.get("")
def form():
    return render_template(
        "upload/form.html",
        max_size=current_app.config['MAX_CONTENT_LENGTH']
    )


@bp.post("")
def upload():
    def check_file_id(length: int = 2):
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
        name=secure_filename(target.filename),
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

    return redirect(url_for("file.show", file_id=file_id))
