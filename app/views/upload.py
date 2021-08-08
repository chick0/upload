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
from app.custom_error import *


bp = Blueprint(
    name="upload",
    import_name="upload",
    url_prefix="/",
)


@bp.get("")
def form():
    return render_template(
        "upload/form.html",
        count=list(storage.keys()).__len__(),
        max=current_app.config['MAX_UPLOAD'],
        max_size=current_app.config['MAX_CONTENT_LENGTH']
    )


@bp.post("")
def upload():
    def check_file_id():
        new_id = token_bytes(4).hex()
        if new_id not in storage.keys():
            return new_id
        else:
            return check_file_id()

    if list(storage.keys()).__len__() >= current_app.config['MAX_UPLOAD']:
        raise TooManyFiles

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
