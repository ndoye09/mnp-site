#!/usr/bin/env python3
import http.server
import socketserver
import os
from pathlib import Path

# Changez vers le répertoire du site
os.chdir(Path(__file__).parent)

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"✅ Serveur démarré sur http://localhost:{PORT}")
    print(f"📂 Répertoire: {os.getcwd()}")
    print(f"🌐 Ouvrez http://localhost:{PORT} dans votre navigateur")
    print(f"⛔ Appuyez sur Ctrl+C pour arrêter le serveur")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✋ Serveur arrêté")
