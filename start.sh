#!/bin/bash

# Lancer le serveur MCP en arrière-plan avec Gunicorn
gunicorn --bind 0.0.0.0:10000 mcp_server:app &

# Lancer le client Discord en premier plan
python3 discord_client_mcp.py