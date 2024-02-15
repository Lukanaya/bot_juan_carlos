# Réalisé par @lukanaya dans le cadre de son service civique, en cas de problèmes, le contacter sur discord
# Si besoin d'un nouveau token ou d'un transfert de propriété, demander à @lukanaya

import discord, re
from discord import app_commands

#on ouvre le fichier contenant le token du bot
fichier_token = open('token', 'r')
token = fichier_token.read()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client) # On déclare la possibilité d'utiliser des commandes slash

#regex pour déterminer par quel mots le message doit commencer pour que le bot réagisse par une émote
pattern_bonjour = re.compile("(?i)(salut|bonjour|yo|coucou|hey|hola|hello|cc|bonsoir)")

@client.event
async def on_ready():
    await tree.sync() #on synchronise les commandes disponibles avec le client discord
    print(f'connecté en tant que {client.user}')

#les différents évènements à réaliser après un message
@client.event 
async def on_message(message):
    if message.author == client.user:
        return

    emote="👋"

    #faire réagir le bot aux messages pour dire bonjour
    if pattern_bonjour.match(message.content.split()[0]):
        await message.add_reaction(emote)

#commande de test
@tree.command(
        name="test",
        description="ceci est un test"
)
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("test", ephemeral=True)

#message envoyé quand un membre rejoint le serveur discord
@client.event
async def on_member_join(member):
    channel = await client.fetch_channel(553923746277359619)
    await channel.send("Bienvenue <@" + str(member.id) + "> ! Tu peux te présenter dans le salon <#553937321146318849> en expliquant ton projet. :smile:")

#Lancement du bot avec son token, si il ne marche plus, contacter @lukanaya sur discord
client.run(token)