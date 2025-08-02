FROM python:3.13-slim AS builder

ENV POETRY_VERSION=2.0.1 \
    POETRY_HOME=/opt/poetry \
    VENV_PATH=/opt/venv \
    PATH="/opt/poetry/bin:/opt/venv/bin:$PATH" \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl build-essential \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false \
    && python -m venv $VENV_PATH \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY pyproject.toml poetry.lock README.md ./
COPY dnswatch ./dnswatch

RUN . $VENV_PATH/bin/activate \
    && poetry install --no-interaction --no-root --only main \
    && poetry build -f sdist \
    && pip install dist/dnswatch-*.tar.gz

FROM python:3.13-slim AS runtime

ENV PATH="/opt/venv/bin:$PATH" \
    VENV_PATH=/opt/venv

COPY --from=builder $VENV_PATH /opt/venv

# Remove unnecessary vulnerable packages
RUN apt remove --purge -y libsqlite3-0 \
    && apt-get autoremove --purge -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY etc/dnswatch.conf.sample /app/dnswatch.conf

WORKDIR /app

ENTRYPOINT ["dnswatch", "--config-file", "/app/dnswatch.conf"]
