import os
import requests
import json
from dotenv import load_dotenv
from datetime import date

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

def get_today_tasks():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    headers = {
        "Authorization": "Bearer " + NOTION_TOKEN,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    
    payload = {
        "filter": {
            "and": [
                {
                    "property": "Date", 
                    "date": {
                        "equals": str(date.today())
                    }
                },
                {
                    "property": "Statut", 
                    "select": {
                        "does_not_equal": "☑️ Terminé"
                    }
                },
            ]
        },
        "sorts": [
            {
                "property": "Date",
                "direction": "ascending"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Erreur API Notion : {response.status_code} - {response.text}"
    
    data = response.json()
    return data["results"]
