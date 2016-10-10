import asyncio
import random

async def on_command(client, message, args):
    if message.channel.is_private: return
    if args[0] == 'roulette':
        if message.author.server_permissions.manage_channels:
            participants = []
            for member in message.server.members:
                if member.status == 'online' and not member.bot:
                    perms = message.channel.permissions_for(member)
                    if perms.read_messages:
                        participants.append(member)
            roll = random.randint(0, len(participants))
            winner = participants[roll]
            await client.send_message(message.channel, "And the winner is: " + winner.mention + "!")
