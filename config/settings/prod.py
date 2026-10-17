from .base import *  # noqa: F401,F403

DEBUG = False

DATABASES = {
    'default': env.db('DATABASE_URL'),
}
# Persistent connections — without this, Django opens a fresh Postgres
# connection on every single request, which is real overhead under load
# behind gunicorn's multiple workers.
DATABASES['default']['CONN_MAX_AGE'] = 600
DATABASES['default']['CONN_HEALTH_CHECKS'] = True

# The app sits behind nginx in the Docker deployment, which terminates TLS
# and proxies to gunicorn over plain HTTP. Without SECURE_PROXY_SSL_HEADER,
# Django can't tell the original request was HTTPS, so SECURE_SSL_REDIRECT
# below would redirect-loop forever (every proxied request looks insecure).
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# Env-overridable, defaulting to the secure/correct production values.
# The bundled docker/nginx.conf terminates plain HTTP on :80 (no TLS certs
# to ship without a real domain — that's the deployer's call, same reason
# object storage was left unwired in Phase 12). Deployed as-is behind real
# TLS (nginx with certs, or a cloud load balancer), the defaults below are
# exactly right and don't need touching. Running the bundled stack over
# plain HTTP only (e.g. a first smoke test before TLS is set up) needs
# SECURE_SSL_REDIRECT=False in .env, or every request redirect-loops.
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Required in prod: the real domain(s) this serves, e.g.
# CSRF_TRUSTED_ORIGINS=https://thebasics.example.com
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

# Redis — used for the cache framework (see apps.core.context_processors
# .footer_subjects for what actually goes through it today). Requires the
# `redis` package (already in requirements/base.txt) — Django's cache
# backend is native since 4.0, no third-party django-redis needed.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('REDIS_URL'),
    },
}

# Real SMTP for password-reset emails — without this, Django falls back to
# its default backend, which needs EMAIL_HOST set anyway or every send()
# raises. dev.py uses the console backend instead; this is the one place
# that actually needs real mail delivery.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@thebasics.local')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {'handlers': ['console'], 'level': 'INFO'},
    'loggers': {
        'django.request': {'handlers': ['console'], 'level': 'ERROR', 'propagate': False},
        'django.security': {'handlers': ['console'], 'level': 'WARNING', 'propagate': False},
        'apps': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
    },
}
