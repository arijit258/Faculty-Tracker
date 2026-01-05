"""
WSGI config for faculty_tracker project.
Faculty Tracker for Easy2Learning Institute
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faculty_tracker.settings')
application = get_wsgi_application()
