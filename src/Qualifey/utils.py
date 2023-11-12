import sys

def is_migration():
    return 'makemigrations' in sys.argv or 'migrate' in sys.argv