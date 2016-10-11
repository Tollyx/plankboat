import asyncio
import random
import discord

async def on_command(client, message, args):
    if message.channel.is_private: return
    if args[0] == 'roulette':
        if message.author.server_permissions.manage_channels:
            participants = []
            for member in message.server.members:
                if member.bot: continue
                if member.status != discord.Status.online: continue
                perms = message.channel.permissions_for(member)
                if perms.read_messages:
                    participants.append(member)
            roll = random.randint(0, len(participants)-1)
            winner = participants[roll]
            await client.send_message(message.channel, "And the winner is: " + winner.mention + "!")
