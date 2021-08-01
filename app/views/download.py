from io import BytesIO

from flask import Blueprint
from flask import abort
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
        return abort(404)

    return send_file(
        BytesIO(blob),
        mimetype="application/octet-stream",
        as_attachment=True,
        attachment_filename=name
    )
