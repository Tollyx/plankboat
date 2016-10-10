import asyncio
import peewee
import database
import re

class Command(database.BaseModel):
    server = peewee.CharField()
    command = peewee.CharField()
    message = peewee.CharField()

async def on_load(client):
    try:
        Command.create_table()
    except peewee.OperationalError as err:
        print(err)

async def on_command(client, message, args):
    if args[0] == "command":
        if not message.channel.permissions_for(message.author).manage_channels: return
        if len(args) == 1 or args[1] == "help":
            pass # Help text here pls
        elif len(args) >= 3 and args[1] == "add":
            newcmd = None

            # Don't create a new entry for a command that already exists
            commands = Command.select().where(Command.server == message.server.id and Command.command == args[2])
            for cmd in commands:
                newcmd = cmd
            if newcmd == None:
                newcmd = Command()

            newcmd.server = message.server.id
            newcmd.command = args[2]
            newcmd.message = ' '.join(args[3:])
            newcmd.save()
            await client.send_message(message.channel, "Added new command '" + args[2] + "'")

        elif len(args) >= 3 and args[1] == "remove":
            commands = Command.select().where(Command.server == message.server.id and Command.command == args[2])
            for cmd in commands:
                cmd.delete_instance()
                await client.send_message(message.channel, "Deleted command '" + args[2] + "'")
        elif args[1] == "list":
            commands = Command.select().where(Command.server == message.server.id)
            msg = ""
            if len(commands) > 0:
                msg = "**Custom commands on this server:**\n"
                for cmd in commands:
                    msg += cmd.command + ", "
                msg = msg[:-2]
            else:
                msg = "This server doesn't have any custom commands yet."
            await client.send_message(message.channel, msg)
    else:
        commands = Command.select().where(Command.server == message.server.id and Command.command == args[0])
        for cmd in commands:
            await client.send_message(message.channel, cmd.message)