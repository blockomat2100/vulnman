import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

try:
    from vulnman.conf.secret_key import SECRET_KEY
except ImportError:
    from vulnman.core.utils.secret import generate_secret_key
    generate_secret_key(os.path.join(BASE_DIR, 'vulnman/conf/secret_key.py'))
    from vulnman.conf.secret_key import SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
]

ROOT_URLCONF = 'vulnman.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

WSGI_APPLICATION = 'vulnman.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_URL = "account:login"
LOGIN_REDIRECT_URL = "projects:project-list"
LOGOUT_REDIRECT_URL = "account:login"
AUTH_USER_MODEL = 'account.User'


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = './static/'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

STATIC_ROOT = os.path.join(BASE_DIR, "static_files")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Set this to True to avoid transmitting the CSRF cookie over HTTP accidentally.
CSRF_COOKIE_SECURE = True

# Set this to True to avoid transmitting the session cookie over HTTP accidentally.
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True


INSTALLED_APPS = [
    # before django.contrib.admin to support django admin integration
    'modeltranslation',
    # set default templates before django apps to make translations work
    'vulnman_default_templates',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'crispy_forms',
    "crispy_bootstrap5",
    "guardian",
    "corsheaders",
    'django_filters',
    'django_q',
    # 2fa stuff
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',
    # apps
    'apps.account.apps.AccountConfig',
    'apps.reporting.apps.ReportingConfig',
    'apps.projects.apps.ProjectsConfig',
    'apps.methodologies.apps.MethodologiesConfig',
    'apps.findings.apps.FindingsConfig',
    'apps.assets.apps.AssetsConfig',
    'core.apps.CoreConfig',
    'api.apps.ApiConfig',
    'apps.responsible_disc.apps.ResponsibleDiscConfig',
    'apps.checklists.apps.ChecklistsConfig'
]


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

CHECKLIST_REPO = "https://github.com/vulnman/community-checklists"

CUSTOM_CSS_FILE = None

# Reporting
REPORT_COMPANY_INFORMATION = {
    "name": "Vulnman",
    "street": "No Street 54",
    "zip": "123456 Berlin",
    "country": "Germany",
    "homepage": "https://vulnman.github.io",
    "contact": "contact@example.com"
}

# Report Templates
REPORT_TEMPLATES = {
    "default": 'vulnman_default_templates.report_templates.default_template'
}


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
]
AUTH_LDAP_SERVER_URI = None
RESPONSIBLE_DISCLOSURE_MAIL_FROM = "vulnman@example.com"
# delete external users after 90 days (e.g. vendors)
INACTIVE_EXTERNAL_USER_DELETE_DAYS = 90

# Translation settings
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

gettext = lambda s: s
LANGUAGES = (
    ('de', gettext('German')),
    ('en', gettext('English')),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'


Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 2,
    'timeout': 90,
    'retry': 120,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default'
}

ADDITIONAL_PACKAGES = []

TOTP_ENFORCE_2FA = False

RESPONSIBLE_DISCLOSURE_VULNERABILITY_ID_PREFIX = "vulnman-"
RESPONSIBLE_DISCLOSURE_PLANNED_PUBLICATION_INTERVAL = 60
RESPONSIBLE_DISCLOSURE_ADVISORY_TEMPLATES = REPORT_TEMPLATES

try:
    from vulnman.conf.local_settings import *
except ImportError:
    pass


# Enable LDAP authentication backend, if LDAP_SERVER_URI is configured
if AUTH_LDAP_SERVER_URI:
    AUTHENTICATION_BACKENDS.append("django_auth_ldap.backend.LDAPBackend")

# Set the custom packages to be on the first place of INSTALLED_APPS to make translations work
# otherwise django will use the first match
if ADDITIONAL_PACKAGES and isinstance(ADDITIONAL_PACKAGES, list):
    INSTALLED_APPS = ADDITIONAL_PACKAGES + INSTALLED_APPS
