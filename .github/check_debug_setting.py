# check_debug_setting.py

from django.conf import settings
import sys
import os

# Set the Django settings module to your_project_name.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapp.settings")

# Reset Django settings to force reconfiguration
settings._wrapped = None

# Configure Django settings
settings.configure()

if settings.DEBUG:
    sys.exit("ERROR: Debug mode must be set to False for the production environment.")
