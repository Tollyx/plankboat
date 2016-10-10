import asyncio
import re
import random

diceregex = re.compile(r'^(\d*?)?d(\d+?)([\+-]\d+?)?$', re.I)

async def on_command(client, message, args):
    match = diceregex.match(args[0])

    if match:
        amount = int(match.group(1) or 1)
        sides = int(match.group(2))
        add = int(match.group(3) or 0)

        if amount > 999999:
            await client.send_message(message.channel, "Too many dice!")
            return

        value = 0
        dice = []
        for x in range(0, amount):
            roll = random.randint(1, sides)
            dice.append(roll)
            value += roll
        value += add

        if amount > 1 and amount <= 32:
            await client.send_message(message.channel, str(value) + '\t(' + ', '.join(dice) + ')')
        else:
            await client.send_message(message.channel, str(value))
