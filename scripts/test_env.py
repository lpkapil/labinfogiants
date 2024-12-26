import os
import django
import sys

# Add the parent directory of 'myproject' to the Python path
# This allows us to import 'myproject' and access the settings
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

# Setup Django
django.setup()

from dotenv import load_dotenv

load_dotenv()  # This loads variables from your .env file


# Check dot env
print(os.getenv('DB_NAME'))
