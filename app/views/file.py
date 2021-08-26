from json import loads

from flask import Blueprint
from flask import g
from flask import abort
from flask import Response
from flask import render_template

from app import redis
from app.models import File


bp = Blueprint(
    name="file",
    import_name="file",
    url_prefix="/file",
)


@bp.get("/<string:file_id>")
def show(file_id: str):
    from_redis = redis.get(f"chick0/upload:{file_id}")
    if from_redis is None:
        return abort(404)

    from_redis = loads(from_redis)
    file = File(*from_redis)

    g.title = file.name
    return render_template(
        "file/show.html",
        file_id=file_id,
        name=file.name,
        size=file.size,
    )


@bp.get("/<string:file_id>/checksums.txt")
def checksums(file_id: str):
    from_redis = redis.get(f"chick0/upload:{file_id}")
    if from_redis is None:
        return abort(404)

    from_redis = loads(from_redis)
    file = File(*from_redis)

    return Response(
        response="\n".join([
            file.name,
            f"md5sum {file.md5}",
            f"sha1sum {file.sha1}",
            f"sha256sum {file.sha256}",
        ]),
        mimetype="text/plain"
    )
