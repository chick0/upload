from json import loads

from flask import Blueprint
from flask import g
from flask import abort
from flask import request
from flask import session
from flask import url_for
from flask import render_template

from app import redis
from app.tuples import File
from app.tuples import Error

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
        file=file,
        download_url="{host}{path}".format(
            host="{scheme}://{host}".format(scheme=request.scheme, host=request.host),
            path=url_for("download.file", file_id=file_id, fake=file.name),
        )
    )


@bp.get("/<string:file_id>/delete")
def delete(file_id: str):
    from_redis = redis.get(f"chick0/upload:{file_id}")
    if from_redis is None:
        return abort(404)

    file = File(*loads(from_redis))

    if session.get(file_id, "undefined") != file.code:
        return abort(403)

    redis.delete(f"chick0/upload:{file_id}")
    del session[file_id]

    return render_template(
        "error.html",
        error=Error(
            title="파일 삭제",
            subtitle="파일이 삭제되었습니다."
        )
    )
