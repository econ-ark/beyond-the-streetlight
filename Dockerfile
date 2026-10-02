# Reproducible environment for the Beyond the Streetlight REMARK.
#
#   docker build -t beyond-the-streetlight .
#   docker run --rm beyond-the-streetlight                      # ./reproduce.sh
#   docker run --rm beyond-the-streetlight ./reproduce_min.sh   # main pipeline only
#
# The environment is the one pinned in uv.lock, installed with the image's Python.
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.21 /uv /uvx /bin/
ENV UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /remark
COPY . .
RUN uv sync --frozen

CMD ["./reproduce.sh"]
