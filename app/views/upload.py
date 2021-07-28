from time import time
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

from app import storage


bp = Blueprint(
    name="upload",
    import_name="upload",
    url_prefix="/",
)


@bp.get("")
def form():
    return render_template(
        "upload/form.html"
    )


@bp.post("")
def upload():
    def check_file_id():
        new_id = token_bytes(4).hex()
        if new_id not in storage.keys():
            return new_id
        else:
            return check_file_id()

    target = request.files.get("file", None)
    if target is None:
        return redirect(url_for("upload.form"))

    if len(storage) >= current_app.config['MAX_UPLOAD']:
        return render_template(
            "upload/too_many_files.html"
        ), 503

    file_id = check_file_id()
    blob = target.stream.read()
    size = len(blob)

    if size == 0:
        return redirect(url_for("upload.form"))

    if size >= current_app.config['MAX_CONTENT_LENGTH']:
        return render_template(
            "upload/file_is_too_big.html"
        ), 413

    storage[file_id] = {
        "blob": blob,
        "name": secure_filename(target.filename),
        "size": size,
        "md5": md5(blob).hexdigest(),
        "sha1": sha1(blob).hexdigest(),
        "sha256": sha256(blob).hexdigest(),
        "time": time(),
    }

    return redirect(url_for("file.show", file_id=file_id))
