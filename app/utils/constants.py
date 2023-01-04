import os

BASE_URL = os.environ.get('BASE_URL')
# SKIP_TAGS = os.getenv('SKIP_TAGS', '').split()
SKIP_REAL = True
SKIP_TAGS = os.environ.get('SKIP_TAGS', '').split()
