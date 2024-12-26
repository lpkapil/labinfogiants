import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

# Setup Django
django.setup()

from dotenv import load_dotenv

load_dotenv()  # This loads variables from your .env file


# Check dot env
print(os.getenv('DB_NAME'))
