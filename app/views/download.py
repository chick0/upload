from io import BytesIO

from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import send_file

from app import storage


bp = Blueprint(
    name="download",
    import_name="download",
    url_prefix="/download",
)


@bp.get("/<string:file_id>")
def file(file_id: str):
    try:
        blob = storage[file_id]['blob']
        name = storage[file_id]['name']
    except KeyError:
        return redirect(url_for("upload.form"))

    return send_file(
        path_or_file=BytesIO(blob),
        mimetype="application/octet-stream",
        as_attachment=True,
        attachment_filename=name
    )
