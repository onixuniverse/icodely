from icodely.settings.default_settings import *

DEBUG = False

SECRET_KEY = "8axil9*$9=12!+brd0_4o#_!2x=^-e2*it^_$=g+fqe8u7s)6"

ALLOWED_HOSTS.append("icodely.ru")

INTERNAL_IPS = []

INSTALLED_APPS.remove("debug_toolbar")

MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")

RECAPTCHA_PUBLIC_KEY = "6LcrYKIoAAAAAOIdvYegg0w2iJIkAH7CeP9pdz2j"
RECAPTCHA_PRIVATE_KEY = "6LcrYKIoAAAAADhdlDeiaJqVJN-5cwh-8Ca5KYM2"
