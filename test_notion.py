import os
import requests
from dotenv import load_dotenv

# Charge les variables depuis le fichier .env
load_dotenv()

# Récupère les secrets depuis l'environnement
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")

def main():
    """
    Fonction principale pour se connecter à Notion et récupérer le titre d'une page.
    """
    # Vérifie que les clés sont bien présentes
    if not NOTION_TOKEN or not PAGE_ID:
        print("Erreur : Le NOTION_TOKEN ou le PAGE_ID n'a pas été trouvé.")
        print("Assurez-vous d'avoir un fichier .env correct.")
        return # Arrête l'exécution si les clés manquent

    url = f"https://api.notion.com/v1/pages/{PAGE_ID}"
    headers = {
        "Authorization": "Bearer " + NOTION_TOKEN,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    print("Tentative de connexion à l'API de Notion...")

    # Exécute la requête
    response = requests.get(url, headers=headers)

    # Vérifie si la requête a réussi
    if response.status_code == 200:
        data = response.json()
        page_title = data["properties"]["title"]["title"][0]["plain_text"]
        print(f"✅ Connexion réussie ! Le titre de la page est : '{page_title}'")
    else:
        print(f"❌ Échec de la connexion. Statut : {response.status_code}")
        print("Réponse de l'API :", response.text)

# Cette ligne permet d'exécuter la fonction main() quand on lance le script
if __name__ == "__main__":
    main()