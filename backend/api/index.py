import sys
import os

# Add the parent directory to sys.path so we can find the 'app' module
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.main import app

# Vercel needs the app object to be named 'app' by default in the entry file
# but we can also export it clearly
handler = app
