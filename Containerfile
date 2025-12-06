FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.9.15 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy

WORKDIR /build
COPY pyproject.toml uv.lock README.md ./
COPY dnswatch ./dnswatch

RUN uv build --wheel \
  && uv pip install --system dist/dnswatch-*.whl

FROM python:3.13-slim AS runtime

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin/dnswatch /usr/local/bin/dnswatch

COPY etc/dnswatch.conf.sample /app/dnswatch.conf

WORKDIR /app

ENTRYPOINT ["dnswatch", "--config-file", "/app/dnswatch.conf"]
