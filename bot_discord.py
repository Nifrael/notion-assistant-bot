import os
import discord
from dotenv import load_dotenv
from notion_logic import get_today_tasks 

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

def _trier_taches(tasks_list):
    tasks_sorted = {
        "pro": {}, "perso": {}, "autres": {}
    }
    
    for task in tasks_list:
        try:
            props = task["properties"]
            name = props["Nom"]["title"][0]["plain_text"]
            status = props["Statut"]["select"]["name"]
            priority = props["Priorité"]["select"]["name"]
            domain = props["Rubrique"]["select"]["name"]
            
            target_domain = (
                tasks_sorted["pro"] if "Pro" in domain else
                tasks_sorted["perso"] if "Perso" in domain else
                tasks_sorted["autres"]
            )
            target_domain.setdefault(status, {}).setdefault(priority, []).append(name)
        except (KeyError, IndexError):
            continue
            
    return tasks_sorted

def _creer_embeds_par_priorite(tasks_sorted):
    priority_order = ["🔥 Urgent", "⚠️ Important", "🏖️ Tranquille"]
    embeds = []

    for priority in priority_order:
        embed = discord.Embed(
            title=f"LISTE DES TÂCHES ------- {priority}",
            color=discord.Color.red() if priority == "🔥 Urgent" else
                  discord.Color.orange() if priority == "⚠️ Important" else
                  discord.Color.blue()
        )

        def add_tasks_to_embed(category_title, tasks_by_domain):
            value = ""
            for status, status_label in [("🕑 En cours", "En cours"), ("📦 Pas commencé", "À faire")]:
                if tasks_by_domain.get(status) and priority in tasks_by_domain[status]:
                    tasks_str = "\n".join([f"- {t}" for t in tasks_by_domain[status][priority]])
                    value += f"**{status_label} :**\n{tasks_str}\n"
            if value:
                embed.add_field(name=f"------- {category_title} --------", value=value, inline=False)

        add_tasks_to_embed("💼 Rubrique Pro", tasks_sorted["pro"])
        add_tasks_to_embed("🏠 Rubrique Perso", tasks_sorted["perso"])
        add_tasks_to_embed("🎓 Rubrique Cours", tasks_sorted["autres"])

        if embed.fields:
            embeds.append(embed)

    return embeds

def _add_list_task_to_embed(embed, category_title, tasks_dict):
    status_en_cours = "🕑 En cours"
    status_pas_commence = "📦 Pas commencé"
    priority_order = ["🔥 Urgent", "⚠️ Important", "🏖️ Tranquille"]
    value = ""
    def _get_status_section(status_key, header_text, task_style):
        nonlocal value
        if tasks_dict.get(status_key):
            if value: value += "\n"
            value += f"**{header_text} :**\n"
            for priority in priority_order:
                if priority in tasks_dict[status_key]:
                    tasks_str = "\n".join([f"{task_style} {t}" for t in tasks_dict[status_key][priority]])
                    value += f"_{priority}_\n{tasks_str}\n"

    _get_status_section(status_en_cours, "🕑 En cours", "**-**")
    _get_status_section(status_pas_commence, "📦 À faire", "-")
    
    if value:
        embed.add_field(name=f"--- {category_title} ---", value=value, inline=False)

def _creer_embed_tableau_de_bord(tasks_sorted):
    """Crée et retourne un SEUL embed Discord final."""
    embed = discord.Embed(
        title="Tableau de Bord du Jour",
        description="Voici un aperçu de vos objectifs pour aujourd'hui.",
        color=discord.Color.blue()
    )
    _add_list_task_to_embed(embed, "💼 Domaine Professionnel", tasks_sorted["pro"])
    _add_list_task_to_embed(embed, "🏠 Domaine Personnel", tasks_sorted["perso"])
    _add_list_task_to_embed(embed, "🎓 Autres Domaines", tasks_sorted["autres"])

    if not embed.fields:
        embed.description = "Aucune tâche correspondante trouvée pour aujourd'hui."
    return embed

# intents = discord.Intents.default()
# intents.message_content = True
# bot = discord.Client(intents=intents)

# @bot.event
# async def on_ready():
#     print(f'Connecté en tant que {bot.user}')

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     if message.content == '!taches':
#         print("Commande !taches reçue...")
#         tasks_list_raw = get_today_tasks()

#         if isinstance(tasks_list_raw, str):
#             embed = discord.Embed(title="❌ Erreur", description=tasks_list_raw, color=discord.Color.red())
#             await message.channel.send(embed=embed)
#         elif not tasks_list_raw:
#             embed = discord.Embed(title="🎉 Aucune tâche pour aujourd'hui !", color=discord.Color.green())
#             await message.channel.send(embed=embed)
#         else: 
#             tasks_sorted = _trier_taches(tasks_list_raw)
#             embeds = _creer_embeds_par_priorite(tasks_sorted)
#             for embed in embeds:
#                     await message.channel.send(embed=embed)

# print("Lancement du bot...")
# bot.run(DISCORD_BOT_TOKEN)