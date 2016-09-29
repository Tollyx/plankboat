import asyncio
import re
import random

diceregex = re.compile(r'^(\d*?)?d(\d+?)([\+-]\d+?)?$', re.I)

async def on_message(client, message):
    # return if the message doesn't start with a mention
    prefix = client.user.mention
    msg = message.content
    if not msg.startswith(prefix): return
    msg = msg[len(prefix):]
    msg = msg.replace(' ', '') # remove all whitespace
    match = diceregex.match(msg)

    if match:
        #print('DICE:', msg)
        amount = int(match.group(1) or 1)
        sides = int(match.group(2))
        add = int(match.group(3) or 0)

        if amount > 999999:
            await client.send_message(message.channel, "Too many dice!")
            return

        #print('DICE:', 'Intrepeted as ' + str(amount) + 'd' + str(sides) + '+' + str(add))
        value = 0
        dice = []
        for x in range(0, amount):
            roll = random.randint(1, sides)
            dice.append(roll)
            value += roll
        value += add
        #print('DICE:', 'Rolled ' + str(value))
        if amount > 1 and amount <= 32:
            #print('DICE:', str(dice))
            await client.send_message(message.channel, str(value) + '\t' + str(dice))
        else:
            await client.send_message(message.channel, str(value))
