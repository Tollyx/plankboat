import discord
import asyncio
import importlib
import re

# Get your API token here: https://discordapp.com/developers/docs/intro
bottoken = 'token'

# The names of the plugins you want to be enabled. TODO: Make plugins be server-specific
plugins = ['mal', 'dice', 'feeds', 'commands']
commandprefix = '^'

client = discord.Client()

def start():
    global plugmods
    plugmods = []
    for plugin in plugins:
        try:
            m = importlib.import_module('plugins.'+plugin)
        except ImportError as err:
            print("Can't load plugin " + plugin + '!')
            print(err)
            continue

        try:
            client.loop.create_task(m.on_load(client))
        except AttributeError as err:
            print("Cannot start " + plugin + ".on_load")
            print(err)

        plugmods.append(m)

    client.run(bottoken)

@client.event
async def on_ready():
    print('Connected as ' + client.user.name + ' with id ' + client.user.id)

#@client.event
#async def on_member_join(member):
#    server = member.server
#    await client.send_message(server, 'Welcome {0} to {1}!'.format(member.mention, server.name))

@client.event
async def on_message(message):
    if message.author.bot or message.author == client.user: return

    args = False
    if message.content.startswith(commandprefix):
        args = message.content[len(commandprefix):].split()
        if len(args) == 0:
            args = False

    for plugin in plugmods:
        if args:
            try:
                await plugin.on_command(client, message, args)
            except AttributeError as err:
                print(err)
        else:
            try:
                await plugin.on_message(client, message)
            except AttributeError as err:
                print(err)

start()