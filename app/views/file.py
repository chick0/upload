
from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import render_template

from app import storage


bp = Blueprint(
    name="file",
    import_name="file",
    url_prefix="/file",
)


@bp.get("/<string:file_id>")
def show(file_id: str):
    try:
        name = storage[file_id]['name']
        size = storage[file_id]['size']
        md5 = storage[file_id]['md5']
    except KeyError:
        return redirect(url_for("upload.form"))

    return render_template(
        "file/show.html",
        file_id=file_id,
        name=name,
        size=size,
        md5=md5,
    )
