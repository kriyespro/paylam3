# syntax=docker/dockerfile:1

# --- Stage 1: build Tailwind CSS ---
# Tailwind's content scan (tailwind.config.js) needs templates/ and apps/
# present to know which classes survive purging, so those are copied in
# even though this stage never runs Python.
FROM node:20-slim AS tailwind-builder
WORKDIR /app
COPY package.json tailwind.config.js ./
RUN npm install
COPY static/src/css/input.css static/src/css/input.css
COPY templates templates
COPY apps apps
RUN npm run tailwind:build

# --- Stage 2: install Python dependencies ---
# Pillow/psycopg ship manylinux wheels with bundled shared libs, so no
# extra system packages are needed here beyond what python:slim has —
# kept as its own stage anyway so the final image never carries pip's
# build cache or a compiler toolchain.
FROM python:3.12-slim AS python-deps
WORKDIR /app
ENV PIP_NO_CACHE_DIR=1
COPY requirements/base.txt requirements/prod.txt requirements/
RUN pip install --user -r requirements/prod.txt

# --- Stage 3: runtime ---
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/app/.local/bin:${PATH}" \
    DJANGO_SETTINGS_MODULE=config.settings.prod

# Non-root user — the app has no reason to run as root, and Docker images
# that do are a real (if boring) security gap.
RUN useradd --create-home --shell /bin/bash app
WORKDIR /app

COPY --from=python-deps /root/.local /home/app/.local
COPY . .
COPY --from=tailwind-builder /app/static/src/css/output.css static/src/css/output.css

# Everything above runs as root (the default until USER switches it) —
# writing /entrypoint.sh and chmod +x both need root, so they happen here,
# before USER app. Putting them after USER app would fail: the app user
# has no write permission at the filesystem root.
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh \
    && mkdir -p /app/staticfiles /app/media \
    && chown -R app:app /home/app/.local /app

USER app

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-"]
