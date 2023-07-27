import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# Set the Django settings module to your_project_name.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapp.settings")

# Fails secret_key for tests
SECRET_KEY = os.environ.get("SECRET_KEY")

try:
    # Import the Django settings module
    from django.conf import settings
    
    # Check the DEBUG setting
    if settings.DEBUG:
        raise ValueError("ERROR: Debug mode must be set to False for the production environment.")
except ImproperlyConfigured as e:
    # If settings are not configured properly, the script will raise an ImproperlyConfigured exception.
    # Handle the exception as needed, e.g., exit with an error or log the issue.
    # For this example, let's print the error message.
    print(f"ERROR: {e}")
except Exception as e:
    # Handle any other exceptions that may occur during the import or check process.
    # For this example, let's print the error message.
    print(f"ERROR: {e}")
