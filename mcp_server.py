# Fichier: mcp_server.py
from flask import Flask, request, jsonify
from notion_logic import get_today_tasks

# On crée une application web avec Flask
app = Flask(__name__)

# On définit une seule "route" ou "adresse" qui écoutera les demandes
@app.route('/execute-tool', methods=['POST'])
def execute_tool():
    """
    Reçoit une demande, appelle le bon outil et retourne le résultat.
    """
    data = request.json
    tool_name = data.get('tool_name')

    if tool_name == 'get_today_tasks':
        print("Serveur MCP: Reçu demande pour l'outil 'get_today_tasks'")
        # On exécute notre fonction asynchrone et on récupère le résultat
        tasks = get_today_tasks()
        print("Serveur MCP: Tâches récupérées, envoi de la réponse...")
        return jsonify(tasks)
    else:
        return jsonify({"error": "Outil non trouvé"}), 404

# On lance le serveur pour qu'il écoute en permanence
if __name__ == '__main__':
    # L'adresse 0.0.0.0 signifie qu'il est accessible depuis votre réseau local
    app.run(host='0.0.0.0', port=5000)