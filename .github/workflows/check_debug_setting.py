# check_debug_setting.py

from django.conf import settings
import sys

if settings.DEBUG:
    sys.exit("ERROR: Debug mode must be set to False for the production environment.")