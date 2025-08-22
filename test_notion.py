import os
import requests
from dotenv import load_dotenv
import json
from datetime import date # On importe le module pour gérer les dates

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

def get_today_tasks(database_id, token):
    """
    Récupère les tâches d'aujourd'hui qui ont le statut "À faire".
    """
    today_iso = date.today().isoformat() # Récupère la date d'aujourd'hui au format "YYYY-MM-DD"
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    # Le corps de la requête avec notre filtre
    # NOTE : Remplacez "Statut" et "Date" par les noms exacts de vos colonnes si différents
    payload = {
        "filter": {
            "and": [
                {
                    "property": "État", 
                    "status": {
                        "equals": "À faire"
                    }
                },
                {
                    "property": "Date", 
                    "date": {
                        "equals": today_iso
                    }
                }
            ]
        }
    }

    print("Récupération des tâches pour aujourd'hui...")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        tasks = data["results"]
        
        if not tasks:
            print("🎉 Aucune tâche pour aujourd'hui ! Profitez-en bien.")
        else:
            print("✅ Voici vos tâches pour aujourd'hui :")
            for task in tasks:
                # On extrait le nom de la tâche du JSON
                # task_name = task["properties"]["Nom"]["title"][0]["plain_text"]
                print(f"- {task_name}")

    else:
        print(f"❌ Échec de la récupération des tâches. Statut : {response.status_code}")
        print("Réponse de l'API :", response.text)

def main():
    if not NOTION_TOKEN or not DATABASE_ID:
        # ...
        return

    get_today_tasks(DATABASE_ID, NOTION_TOKEN)

if __name__ == "__main__":
    main()