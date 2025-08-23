import os
import discord
import requests
import json
import google.generativeai as genai
import asyncio
from bot_discord import _trier_taches, _add_list_task_to_embed, _creer_embed_tableau_de_bord
from dotenv import load_dotenv

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

tools = [
    {
        "function_declarations": [
            {
                "name": "get_today_tasks",
                "description": "Utilise cet outil pour récupérer la liste des tâches et objectifs à accomplir aujourd'hui dans la base de données Notion de l'utilisateur. Appelle cet outil dès que l'utilisateur pose une question sur son planning, ses tâches, ses objectifs ou sa liste de tâches pour la journée en cours.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {},
                }
            }
        ]
    }
]

def _get_gemini_response_sync(user_message):
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        tools=tools,
        system_instruction="Tu es un assistant dont le seul but est d'appeler les fonctions (outils) que l'on te fournis pour répondre à la demande de l'utilisateur. Ne réponds jamais par du texte simple."
    )
    return model.generate_content(user_message)

def _call_mcp_server_sync(tool_name):
    return requests.post(
        'http://127.0.0.1:5000/execute-tool',
        json={'tool_name': tool_name}
    )


intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'Client MCP connecté en tant que {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith("!"):
        await message.channel.send("Désolé, je ne réponds plus aux commandes classiques. Posez-moi une question.")
        return

    embed = None
    
    try:
        response_gemini = await asyncio.to_thread(_get_gemini_response_sync, message.content)
        
        if not response_gemini.candidates[0].content.parts or not response_gemini.candidates[0].content.parts[0].function_call:
            embed = discord.Embed(
                title="Désolé, je n'ai pas compris",
                description="Je ne sais pas comment utiliser mes outils pour répondre à votre demande. Essayez de reformuler.",
                color=discord.Color.orange()
            )
        else:
            tool_call = response_gemini.candidates[0].content.parts[0].function_call
            tool_name = tool_call.name
            
            print(f"Client MCP: Gemini a demandé l'outil -> {tool_name}")
            
            mcp_server_response = await asyncio.to_thread(_call_mcp_server_sync, tool_name)
            mcp_server_response.raise_for_status()
            tasks_list_raw = mcp_server_response.json()
            
            if isinstance(tasks_list_raw, str):
                embed = discord.Embed(title="❌ Erreur du serveur", description=tasks_list_raw, color=discord.Color.red())
            elif not tasks_list_raw:
                embed = discord.Embed(title="🎉 Aucune tâche pour aujourd'hui !", description="Profitez-en bien.", color=discord.Color.green())
            else:
                tasks_sorted = _trier_taches(tasks_list_raw)
                embed = _creer_embed_tableau_de_bord(tasks_sorted)

    except Exception as e:
        embed = discord.Embed(
            title="❌ Erreur inattendue",
            description=f"Détails : `{e}`",
            color=discord.Color.red()
        )
    
    if embed:
        await message.channel.send(embed=embed)

print("Lancement du client MCP...")
bot.run(DISCORD_BOT_TOKEN)