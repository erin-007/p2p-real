"""
WSGI config for p2p_tutoring project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p2p_tutoring.settings')

application = get_wsgi_application()
