FROM python:3.11.2-slim AS base

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends curl git build-essential make \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME="/opt/poetry" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    SERVICE_HOME=/usr/src/application
ENV PATH="POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

FROM base AS install

# allow controlling the poetry installation of dependencies via external args
ARG INSTALL_ARGS="--only main"
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
COPY pyproject.toml poetry.lock ./

# where your code lives
WORKDIR $SERVICE_HOME

# install without virtualenv, since we are inside a container
RUN poetry config virtualenvs.create false \
    && poetry install $INSTALL_ARGS

# cleanup
RUN curl -sSL https://install.python-poetry.org | python3 - --uninstall
RUN apt-get purge -y curl git build-essential \
    && apt-get clean -y \
    && rm -rf /root/.cache \
    && rm -rf /var/apt/lists/* \
    && rm -rf /var/cache/apt/*

FROM install as app-image

ENV OTEL_PYTHON_FASTAPI_EXCLUDED_URLS="client/.*/info,healthcheck,metrics,docs,openapi.json,redocs"
ENV OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_RESPONSE="content-type"

# copy whole project to your docker home directory.
COPY . ./

EXPOSE 8000

ENTRYPOINT ["make", "run"]
