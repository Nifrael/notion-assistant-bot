# Fichier: daily_reporter.py
import os
import discord
import asyncio
from dotenv import load_dotenv
from notion_logic import get_today_tasks
# Assurez-vous que bot_discord.py est dans le même dossier pour importer ses fonctions
from bot_discord import _trier_taches, _creer_embeds_par_priorite

# --- CONFIGURATION ---
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
# L'ID du canal où le message doit être envoyé
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# --- SCRIPT PRINCIPAL ---
async def send_daily_report():
    intents = discord.Intents.default()
    bot = discord.Client(intents=intents)

    @bot.event
    async def on_ready():
        print(f'Connecté en tant que {bot.user} pour le rapport quotidien.')
        channel = bot.get_channel(DISCORD_CHANNEL_ID)
        
        if not channel:
            print(f"Erreur : Impossible de trouver le canal avec l'ID {DISCORD_CHANNEL_ID}")
            await bot.close()
            return

        tasks_list_raw = get_today_tasks()

        if isinstance(tasks_list_raw, str):
            embed = discord.Embed(title="❌ Erreur", description=tasks_list_raw, color=discord.Color.red())
            await channel.send(embed=embed)
        elif not tasks_list_raw:
            embed = discord.Embed(title="🎉 Aucune tâche pour aujourd'hui !", description="Profitez-en bien.", color=discord.Color.green())
            await channel.send(embed=embed)
        else:
            tasks_sorted = _trier_taches(tasks_list_raw)
            embeds = _creer_embeds_par_priorite(tasks_sorted)
            for embed in embeds:
                await channel.send(embed=embed)

        print("Rapport envoyé. Déconnexion.")
        await bot.close()

    await bot.start(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(send_daily_report())