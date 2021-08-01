
from flask import render_template

from app.custom_error import *


def file_is_empty(e):
    return render_template(
        "error/file_is_empty.html"
    ), 400


def page_not_found(e):
    return render_template(
        "error/page_not_found.html"
    ), 404


def file_is_too_big(e):
    return render_template(
        "error/file_is_too_big.html"
    ), 413


def too_many_files(e):
    return render_template(
        "error/too_many_files.html"
    ), 503


# error map
error_map = {
    404: page_not_found,
    413: file_is_too_big,

    # custom error
    FileIsEmpty: file_is_empty,
    FileIsTooBig: file_is_too_big,
    TooManyFiles: too_many_files,
}
