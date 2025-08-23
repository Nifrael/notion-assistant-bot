#!/bin/bash
# Arrête le script si une commande échoue
set -e

echo "Lancement du serveur Gunicorn en arrière-plan..."
# Lance le serveur web qui écoute les requêtes
gunicorn mcp_server:app --bind 0.0.0.0:10000 &

echo "Lancement du client Discord en premier plan..."
# Lance le client qui se connecte à Discord
python3 discord_client.py