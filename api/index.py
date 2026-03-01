import sys
import os

# On ajoute le dossier 'backend' à sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

# On importe l'application FastAPI
try:
    from app.main import app
except ImportError as e:
    # Aide au debug sur Vercel si l'import échoue
    print(f"DEBUG: sys.path is {sys.path}")
    print(f"DEBUG: current directory is {os.getcwd()}")
    raise e

# C'est l'exportation que Vercel attend pour l'ASGI (FastAPI)
# On ne définit PAS 'handler' car ça peut forcer Vercel vers le mode WSGI
# qui cause l'erreur TypeError: issubclass() arg 1 must be a class
