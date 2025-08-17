from pathlib import Path
import environ
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialise environ
env = environ.Env(
    DEBUG=(bool, True),
)

# Read .env only if it exists (for local dev).
# In Docker, env vars injected by docker-compose override .env.
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(env_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="django-insecure-default-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS", default=["paraxis.com", "localhost", "127.0.0.1", "0.0.0.0"]
)

# Application definition
INSTALLED_APPS = [
    "account.apps.AccountConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "social_django",
    "django_extensions",
    "post.apps.PostConfig",
    "easy_thumbnails",
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "paraxis.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "paraxis.wsgi.application"

# Database (SQLite for now)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = env("TIME_ZONE", default="Asia/Kolkata")
USE_TZ = True
USE_I18N = True

# Static files
STATIC_URL = "static/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email config
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="localhost")
EMAIL_PORT = env("EMAIL_PORT")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="Paraxis <no-reply@paraxis.com>")

# Authentication
LOGIN_REDIRECT_URL = "profile"
LOGIN_URL = "login"
LOGOUT_URL = "logout"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

CSRF_FAILURE_VIEW = "account.views.custom_csrf_failure_view"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "account.authentication.EmailAuthBackend",
    "social_core.backends.twitter.TwitterOAuth",
    "social_core.backends.google.GoogleOAuth2",
]

# Social auth keys
SOCIAL_AUTH_TWITTER_KEY = env("SOCIAL_AUTH_TWITTER_KEY", default=None)
SOCIAL_AUTH_TWITTER_SECRET = env("SOCIAL_AUTH_TWITTER_SECRET", default=None)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", default=None)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", default=None)

# Social auth pipeline
SOCIAL_AUTH_PIPELINE = [
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "account.authentication.create_profile",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
]

# Canonical URLs for models
ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda u: reverse_lazy("user_detail", args=[u.username])
}

# HTTPS/secure settings
SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

INTERNAL_IPS = ["127.0.0.1"]

# Redis config
REDIS_HOST = env("REDIS_HOST", default="127.0.0.1")
REDIS_PORT = env("REDIS_PORT")
REDIS_DB = env("REDIS_DB")
