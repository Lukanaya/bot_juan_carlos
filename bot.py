# Réalisé par @lukanaya dans le cadre de son service civique, en cas de problèmes, le contacter sur discord
# Si besoin d'un nouveau token ou d'un transfert de propriété, demander à @lukanaya

from datetime import datetime, date, time
import discord, re
from discord import app_commands
from discord.ext import commands

#on ouvre le fichier contenant le token du bot
fichier_token = open('token', 'r')
token = fichier_token.read()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

departPersonnel = 0 #Date de départ du personnel du fablab
retourPersonnel = 0 #Date de retour

#regex pour déterminer par quel mots le message doit commencer pour que le bot réagisse par une émote
pattern_bonjour = re.compile("(?i)(salut|bonjour|yo|coucou|hey|hola|hello|cc|bonsoir)")

@bot.event
async def on_ready():
    await bot.tree.sync() #on synchronise les commandes disponibles avec le client discord
    print(f'connecté en tant que {bot.user}')

#les différents évènements à réaliser après un message
@bot.event 
async def on_message(message):
    if message.author == bot.user:
        return

    emote="👋"

    #faire réagir le bot aux messages pour dire bonjour
    if pattern_bonjour.match(message.content.split()[0]):
        await message.add_reaction(emote)

#commande pour paramétrer une abscence du personnel du fablab, un adhérent pourra après utiliser une commande pour vérifier si le fablab est ouvert.
#cette commande nécessite le role "Staff" sur le discord d'innofab pour être utilisée
@bot.tree.command(
        name="absence",
        description="Permet de définir une date d'absence du personnel du fablab.")
@app_commands.describe(depart="Optionnel : La date du début d'absence du personnel (en format unix timestamp)")
@app_commands.describe(retour="Optionnel : L'heure de retour du personnel (en format unix timestamp)")
async def absence(interaction: discord.Interaction, depart: int = int(datetime.now().timestamp()), retour: int = None):
    role_requis = "Staff"
    if not(discord.utils.get(interaction.user.roles, name=role_requis)): #On vérifie si l'utilisateur a un rôle appelé "Staff", si il ne l'a pas, on le prévient et on n'exécute pas la commande
        await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)
        return
    global departPersonnel
    departPersonnel = depart
    dateDepart = datetime.fromtimestamp(depart)
    global retourPersonnel
    if retour is None: #On vérifie si l'utilisateur a rentré une date de retour, si non, on prend la fin du jour actuel
        retourPersonnel = int(datetime.timestamp(datetime.combine(dateDepart, time.max)))
        await interaction.response.send_message(f"Le personnel du fablab sera absent le <t:{depart}:d>.")
    else:
        retourPersonnel = retour
        await interaction.response.send_message(f"Le personnel du fablab sera absent le <t:{depart}:d> de <t:{depart}:t> à <t:{retour}:t>.")

#Affiche à l'utilisateur ayant utilisé la commande, et seulement lui, un message disant si le fablab est ouvert ou non en fonction de l'absence paramétrée par le staff
@bot.tree.command(
        name="fablab_ouvert",
        description="Affiche si le fablab est ouvert ou non, et si il est fermé, quand il sera à nouveau ouvert.")
async def fablab_ouvert(interaction: discord.Interaction):
    global retourPersonnel
    global departPersonnel
    depart = departPersonnel
    retour = retourPersonnel
    if (depart <= int(datetime.now().timestamp())) and (int(datetime.now().timestamp()) <= retour):
        await interaction.response.send_message(f"Le fablab est fermé le <t:{depart}:d> de <t:{depart}:t> à <t:{retour}:t>.", ephemeral=True)
    else :
        await interaction.response.send_message(f"Le fablab est actuellement ouvert !", ephemeral=True)

#message envoyé quand un membre rejoint le serveur discord
@bot.event
async def on_member_join(member):
    channel = await bot.fetch_channel(553923746277359619)
    await channel.send("Bienvenue <@" + str(member.id) + "> ! Tu peux te présenter dans le salon <#553937321146318849> en expliquant ton potentiel projet. :smile:")

#Lancement du bot avec son token, si il ne marche plus, contacter @lukanaya sur discord
bot.run(token)