FROM python:{{ cookiecutter.python_version }} as poetry
MAINTAINER Harrison Totty <harrisongtotty@gmail.com>

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=false \
    POETRY_VERSION={{ cookiecutter.poetry_version }} \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

RUN pip install "poetry==$POETRY_VERSION"

FROM poetry as import_project

ADD . /project

WORKDIR /project

FROM import_project as build_tests

RUN poetry install \
    --no-interaction \
    --no-ansi

RUN pytest tests

FROM import_project as build_release

RUN poetry install \
    --no-dev \
    --no-interaction \
    --no-ansi

FROM build as runtime

CMD kopf run -A -m {{ cookiecutter.module_name }}
