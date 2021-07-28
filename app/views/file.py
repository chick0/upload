
from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import Response
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
    except KeyError:
        return redirect(url_for("upload.form"))

    return render_template(
        "file/show.html",
        file_id=file_id,
        name=name,
        size=size,
    )


@bp.get("/<string:file_id>/checksums.txt")
def checksums(file_id: str):
    try:
        name = storage[file_id]['name']
        md5 = storage[file_id]['md5']
        sha1 = storage[file_id]['sha1']
        sha256 = storage[file_id]['sha256']
    except KeyError:
        return redirect(url_for("upload.form"))

    return Response(
        response="\n".join([
            name,
            f"md5sum {md5}",
            f"sha1sum {sha1}",
            f"sha256sum {sha256}",
        ]),
        mimetype="text/plain"
    )
