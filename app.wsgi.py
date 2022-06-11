import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '')
from app import app as application
application.root_path = ''
application.secret_key = ''