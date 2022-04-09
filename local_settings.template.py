# This is an example settings file for vulnman


# Enable debug mode. DONT USE IN PRODUCTION ENVIRONMENT!
# DEBUG = True

# Allowed Hosts
# set this to the hostnames of allowed to be used in the Host HTTP header
# ALLOWED_HOSTS = ["vulnman.example.com"]

# Required Setting:
# CSRF_TRUSTED_ORIGINS = ['http://localhost','http://127.0.0.1']


# CSS theme
# VULNMAN_CSS_THEME = "flatly"

# #################
# Database Settings
# #################
# uncomment the postgres section, if you are using the docker image
#
# Postgres Example:
#
# DATABASES = {
#  'default': {
#    'ENGINE': 'django.db.backends.postgresql',
#    'HOST': 'db',
#    'NAME': 'vulnman',
#    'USER': 'vulnman_db_user',
#    'PASSWORD': 'dontusethispassword',
#  }
# }


# #########
# Reporting
# #########

# Report Template
# REPORTING_TEMPLATE = "custom.report_templates.bugbounty.BugBountyReportTemplate"


# Add information about your company that is displayed in the report
# REPORT_COMPANY_INFORMATION = {
#     "name": "Vulnman",
#     "street": "No Street 54",
#     "zip": "123456 Berlin, Germany",
#     "homepage": "https://vulnman.github.io/vulnman",
#     "contact": "contact@example.com"
# }


# ########
# Security
# For further harding checks see https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
# Note: the SECRET_KEY value is uniquely auto generated by default for vulnman installations
# ########

# Set this to True to avoid transmitting the CSRF cookie over HTTP accidentally.
# Default: True
# CSRF_COOKIE_SECURE = True

# Set this to True to avoid transmitting the session cookie over HTTP accidentally.
# Default: True
# SESSION_COOKIE_SECURE = True


######################
# Celery Worker
######################
# Required for Docker!
# CELERY_BROKER_URL = "redis://redis:6379"
# CELERY_RESULT_BACKEND = "redis://redis:6379"
