import discord
import time
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
client = discord.Client()
@bot.command(pass_context=True, name='join', help='Te rejoins dans un channel audio')
async def join(ctx):
    user = ctx.message.author
    channel = user.voice.channel
    await channel.connect()

@bot.command(pass_context=True, name='leave', help='Dégage d\'un channel audio')
async def leave(ctx):
    for x in bot.voice_clients:
        if (x.guild == ctx.message.guild):
            await x.disconnect()

#Pendant le débat
@bot.command(pass_context=True, name='debate', help='Temps de débat')
async def debate(ctx):
    debate_time = 120 #temps du débat
    global_time_begin = 35 #temps de discussion générale au début
    global_time_end = 20 #temps de discussion générale à la fin
    time_each = 12  # temps par joueur par tour
    for x in bot.voice_clients:#Partout où est le bot
        if (x.guild == ctx.message.guild):#Si je suis dans le meme monde que là où j'ai été appel"
            channel = x.channel #gets the channel you want to get the list from
            await ctx.send("Début du débat !!! :gun:")
            members = channel.members #finds members connected to the channel
            players = [] #(list)
            for member in members:
                roles_name = [role.name for role in member.roles]
                if "Bots" not in roles_name and "Morts" not in roles_name: #si les jours ont pas le role Bots ou Morts je l'ajoute à ma liste de joeur
                    players.append(member)
            await ctx.send("Débat général pendant {} secondes".format(global_time_begin))
            for player in players:
                roles_name= [role.name for role in player.roles]
                if "Bots" not in roles_name and "Morts" not in roles_name:
                    await player.edit(mute=False) #Je démute tout le monde (les vivants)
            time.sleep(global_time_begin)#Pause dans le script le temps que les gens parlent
            for player in players:#Je remute tous les joueurs
                await player.edit(mute=True)
            time_each = (debate_time-(global_time_begin+global_time_end))/len(players)
            await ctx.send("Temps de parole par personnes : {}".format(time_each))
           # for _ in range(int((debate_time-(global_time_begin+global_time_end))/(time_each*len(players)))): #Je boucle tant qu'il me reste du temps
            for player in players:
                roles_name = [role.name for role in player.roles]
                if "Bots" not in roles_name and "Morts" not in roles_name:
                    mess = "Au tour de @{} : ".format(player.name)
                    await ctx.send(mess)
                    await player.send('À ton tour de parler 👀 !')#Je text le boy pour lui dire que c'est son tour
                    await player.edit(mute=False)#Je le demute
                    time.sleep(time_each)#Je le laisse parler son temps
                    await player.edit(mute=True)#Et je le remute
                    await player.send('Aller stopppp 👀 !')
            await ctx.send("Début de la phase globale  pendant {} secondes".format(global_time_end))
            for player in players:
                roles_name = [role.name for role in player.roles]
                if "Bots" not in roles_name and "Morts" not in roles_name:              #Je laisse parler tout le monde
                    await player.send('Tu peux parler 👀 !')
                    await player.edit(mute=False)
            time.sleep(global_time_end)
            await ctx.send("Et chut")
            for player in players: #Tout le monde se tait
                await player.send('Aller chuttt 👀 !')
                await player.edit(mute=True)

@bot.command(pass_context=True, name='start', help='Mute tout le monde')
async def start(ctx):
    for x in bot.voice_clients:
        if (x.guild == ctx.message.guild):
            channel = x.channel  # bot.get_channel(x.channel) #gets the channel you want to get the list from
            members = channel.members  # finds members connected to the channel
            players = []  # (list)
            for member in members:
                print(member)
                if "Bots" not in [role.name for role in member.roles]:
                    players.append(member)
            for player in players:
                await player.edit(mute=True)

@bot.command(pass_context=True, name='unmute', help='Unmute tout le monde')
async def unmute(ctx):
    print(ctx)
    for x in bot.voice_clients:
        if (x.guild == ctx.message.guild):
            channel = x.channel  # bot.get_channel(x.channel) #gets the channel you want to get the list from
            members = channel.members  # finds members connected to the channel
            players = []  # (list)
            for member in members:
                players.append(member)
            for player in players:
                await player.edit(mute=False)

@bot.command(name="game", help="Lance une nouvelle game")
async def game(ctx):
    msg = await ctx.channel.history(limit=50).flatten()
    for m in msg:
        await m.delete()
    msg = await ctx.send("Que la game commence ! \n Utilise :mute: pour mute tout le monde, :loud_sound: pour unmute, :knife: pour t'ajouter aux morts, :repeat: pour recommencer une game ou :man_detective: pour lancer un débat. \n\nPS SEUL LE AJOUTER AU MORT MARCHE ACTUELLEMENT, deso pas deso")
   # await msg.add_reaction(emoji="mute:423541694600970243")
    await msg.add_reaction('🔇')
    await msg.add_reaction("🔊")
    await msg.add_reaction("🔪")
    await msg.add_reaction("🔁")
    await msg.add_reaction("🕵️‍♂️")

@bot.event
async def on_reaction_add(reaction, user):
    emoji = reaction.emoji
    channel= reaction.message.channel
    if user.bot:
        return

    if emoji == "🔇":
        print("I have to mute everyone")
        await channel.send("!start")
    elif emoji == "🔊":
        print("I have to unmute everyone")
        await channel.send("!unmute")
    elif emoji == "🔪":
        print("I have to add the guy to dead")
        role = discord.utils.get(user.guild.roles, name="Morts")
        await user.add_roles(role)
        await user.edit(mute=True)
    elif emoji == "🔁":
        print("I have to unmute everyone and refaire vivre tout le monde")
        await channel.send("!unmute")
    elif emoji == "🕵️‍♂️":
        print("I have to lancer le débat")
        await channel.send("!debate")
    else:
        return

@bot.event
async def on_reaction_remove(reaction, user):
    emoji = reaction.emoji

    if user.bot:
        return

    if emoji == "🔪":
        print("I have to add the guy to dead")
        role = discord.utils.get(user.guild.roles, name="Morts")
        await user.remove_roles(role)
        await user.edit(mute=False)
    else:
        return

bot.run(TOKEN)
