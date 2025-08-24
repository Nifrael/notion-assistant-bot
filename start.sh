#!/bin/bash
set -e

echo "Lancement du serveur Gunicorn en arrière-plan..."
gunicorn mcp_server:app --bind 0.0.0.0:10000 &

echo "Lancement du client Discord en mode 'relance'..."
# La boucle 'while true' relancera le bot s'il plante
while true
do
    python3 discord_client.py
    echo "Le bot a planté. Redémarrage dans 5 secondes..."
    sleep 5
done