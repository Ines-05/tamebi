import sys
import os

# On ajoute le dossier 'backend' pour que Python trouve nos modules 'app'
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.main import app

# Vercel utilise cet objet 'app' pour lancer le serveur
handler = app
