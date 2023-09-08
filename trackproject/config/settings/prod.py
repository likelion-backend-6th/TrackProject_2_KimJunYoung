from .base import *

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [
    "lion-lb-staging-19480416-c5464abf6647.kr.lb.naverncp.com",
]

CSRF_TRUSTED_ORIGINS = [
    "http://lion-lb-staging-19480416-c5464abf6647.kr.lb.naverncp.com",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "postgres"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.getenv("DB_HOST", "db"),
    }
}
