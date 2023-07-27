import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# Set the Django settings module to your_project_name.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")

try:
    # Try to configure Django settings if not already configured
    settings.configure()
    # Check the DEBUG setting
    if settings.DEBUG:
        raise ValueError("ERROR: Debug mode must be set to False for the production environment.")
except ImproperlyConfigured as e:
    # If settings are already configured, the script is being run within the Django context.
    # You can handle it as needed, e.g., exit with an error or log the issue.
    # For this example, let's print the error message.
    print(f"ERROR: {e}")
