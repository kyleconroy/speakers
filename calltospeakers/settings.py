"""
Django settings for calltospeakers project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os

from configurations import Configuration, values


class Common(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    TEMPLATE_DIRS = (
        BASE_DIR + '/templates/',
    )

    STATIC_ROOT = BASE_DIR + "/static/"

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)

    TEMPLATE_DEBUG = values.BooleanValue(DEBUG)

    ALLOWED_HOSTS = []

    # Application definition
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'social.apps.django_app.default',
        'markdown_deux',
        'cfp',
    )

    MIDDLEWARE_CLASSES = (
        'djangosecure.middleware.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'social.apps.django_app.context_processors.backends',
        'social.apps.django_app.context_processors.login_redirect',
        'cfp.context_processors.empty_profile',
    )

    ROOT_URLCONF = 'calltospeakers.urls'

    WSGI_APPLICATION = 'calltospeakers.wsgi.application'

    LOGIN_REDIRECT_URL = '/'

    # Internationalization
    # https://docs.djangoproject.com/en/1.6/topics/i18n/
    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.6/howto/static-files/
    STATIC_URL = '/static/'

    DATABASES = values.DatabaseURLValue(
        'sqlite:///{}'.format(os.path.join(BASE_DIR, 'db.sqlite3'))
    )

    SOCIAL_AUTH_GITHUB_KEY = values.Value()
    SOCIAL_AUTH_GITHUB_SECRET = values.Value()
    SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']

    SOCIAL_AUTH_TWITTER_KEY = values.Value()
    SOCIAL_AUTH_TWITTER_SECRET = values.Value()

    MAILGUN_KEY = values.Value()

    AUTHENTICATION_BACKENDS = (
        #'social.backends.twitter.TwitterOAuth',
        'social.backends.github.GithubOAuth2',
        'django.contrib.auth.backends.ModelBackend',
    )


class Development(Common):
    """
    The in-development settings and the default configuration.
    """
    DEBUG = True
    TEMPLATE_DEBUG = True

    ALLOWED_HOSTS = []

    INSTALLED_APPS = Common.INSTALLED_APPS + (
        'debug_toolbar',
    )


class Production(Common):
    """
    The production settings.
    """
    INSTALLED_APPS = Common.INSTALLED_APPS + (
        'djangosecure',
        'raven.contrib.django.raven_compat',
    )

    ALLOWED_HOSTS = [
        'speakers.herokuapp.com',
        'calltospeakers.com',
        'www.calltospeakers.com',
    ]

    # django-secure
    SESSION_COOKIE_SECURE = values.BooleanValue(True)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)
    SECURE_HSTS_SECONDS = values.IntegerValue(31536000)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_FRAME_DENY = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SECURE_PROXY_SSL_HEADER = values.TupleValue(
        ('HTTP_X_FORWARDED_PROTO', 'https')
    )
