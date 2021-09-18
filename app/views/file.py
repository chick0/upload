from json import loads
from hashlib import md5

from flask import Blueprint
from flask import g
from flask import abort
from flask import request
from flask import Response
from flask import render_template

from app import redis
from app.models import File
from app.models import Error
from app.secret_key import SECRET_KEY


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


@bp.get("/<string:file_id>/delete")
def delete(file_id: str):
    key_from_user = request.cookies.get(file_id, None)
    if key_from_user is None:
        return abort(403)

    from_redis = redis.get(f"chick0/upload:{file_id}")
    if from_redis is None:
        return abort(404)

    from_redis = loads(from_redis)
    file = File(*from_redis)

    key = md5(file.md5.encode() + SECRET_KEY + file_id.encode()).hexdigest()

    if key != key_from_user:
        return abort(403)

    redis.delete(f"chick0/upload:{file_id}")

    return render_template(
        "error.html",
        error=Error(
            title="파일 삭제",
            subtitle="파일이 삭제되었습니다."
        )
    )
