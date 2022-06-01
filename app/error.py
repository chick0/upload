from flask import current_app
from flask import render_template

from app.custom_error import *
from app.template_filter import display_size
from app.tuples import Error


def forbidden(e):
    return render_template(
        "error.html",
        error=Error(
            title="403",
            subtitle="권한이 부족합니다."
        )
    ), 403


def page_not_found(e):
    return render_template(
        "error.html",
        error=Error(
            title="404",
            subtitle="해당 파일을 찾을 수 없습니다."
        )
    ), 404


def file_is_too_big(e):
    max_size = display_size(current_app.config['MAX_CONTENT_LENGTH'])
    return render_template(
        "error.html",
        error=Error(
            title="파일 업로드 실패",
            subtitle=f"업로드 가능한 가장 큰 파일의 크기는 <b>{max_size}</b>입니다."
        )
    ), 413


def file_is_empty(e):
    return render_template(
        "error.html",
        error=Error(
            title="파일 업로드 실패",
            subtitle="업로드 할 파일을 발견하지 못했습니다."
        )
    ), 400


# error map
error_map = {
    403: forbidden,
    404: page_not_found,
    413: file_is_too_big,

    # custom error
    FileIsEmpty: file_is_empty,
    FileIsTooBig: file_is_too_big
}
