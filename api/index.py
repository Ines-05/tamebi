import sys
import os

# Base directory for the root of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_PATH = os.path.join(BASE_DIR, "backend")

# Ensure 'backend' is in sys.path BEFORE importing the app
if BACKEND_PATH not in sys.path:
    sys.path.append(BACKEND_PATH)

print(f"DEBUG: Vercel - BASE_DIR: {BASE_DIR}")
print(f"DEBUG: Vercel - sys.path updated: {sys.path}")

# Import the FastAPI application
try:
    from app.main import app
except ImportError as e:
    print(f"DEBUG: Vercel - Current dir: {os.getcwd()}")
    print(f"DEBUG: Vercel - List dir: {os.listdir(os.getcwd())}")
    if os.path.exists(BACKEND_PATH):
        print(f"DEBUG: Vercel - Backend exists at {BACKEND_PATH}")
        print(f"DEBUG: Vercel - Backend contents: {os.listdir(BACKEND_PATH)}")
    raise e

# Required: The variable must be named 'app' for Vercel to find it as an ASGI app
# (already correct since it's imported as 'app')
