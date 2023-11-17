from icodely.settings.default_settings import *

DEBUG = False

SECRET_KEY = ""

ALLOWED_HOSTS.append("icodely.ru")

INTERNAL_IPS = []

INSTALLED_APPS.remove("debug_toolbar")

MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")

RECAPTCHA_PUBLIC_KEY = ""
RECAPTCHA_PRIVATE_KEY = ""
