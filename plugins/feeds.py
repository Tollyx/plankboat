import asyncio
import requests
import feedparser
import time
import peewee
import discord
import database
import re

updaterate = 60*15

lastupdate = None

class Feed(database.BaseModel):
    url = peewee.CharField()
    channel = peewee.CharField()
    server = peewee.CharField()

async def on_load(client):
    lastupdate = time.gmtime()
    await client.wait_until_ready()

    try:
        Feed.create_table()
    except peewee.OperationalError as err:
        print(err)

    # feed update loop
    while not client.is_closed:
        print("FEED: Checking feed updates...")
        for feed in Feed.select():
            d = feedparser.parse(feed.url)
            if d.status == 200:
                for entry in d.entries:
                    upd = None
                    try:
                        upd = entry.published_parsed
                    except Exception as e:
                        try:
                            upd = entry.updated_parsed
                        except Exception as e:
                            print(e)

                    if not upd:
                        print("Cannot find updated field in feed '" + d.feed.title + "'!")
                        break

                    if upd > lastupdate:
                        msg = '**' + d.feed.title + '**\n*' + entry.title + '*\n' + entry.link
                        server = discord.utils.find(lambda s: s.id == feed.server, client.servers)
                        if server:
                            channel = discord.utils.find(lambda c: c.id == feed.channel, server.channels)
                            if channel:
                                await client.send_message(channel, msg)
            await asyncio.sleep(1)
        lastupdate = time.gmtime()
        await asyncio.sleep(updaterate)

feedre = re.compile(r"\s*feed\s+(\S+)\s*(\S*)")

async def on_command(client, message, args):
    perms = message.channel.permissions_for(message.author)

    if args[0] == 'feed':
        # Add feed to the current channel
        if args[1] == "add":
            if not perms.manage_channels:
                return
            if not len(args[2]) > 0:
                await client.send_message(message.channel, "You need to give me a link to the feed you want to add, dear sir.")
                return
            if not message.channel.is_private:
                try:
                    d = feedparser.parse(args[2])
                    if d.status == 200:
                        newfeed = Feed()
                        newfeed.url = args[2]
                        newfeed.channel = message.channel.id
                        newfeed.server = message.server.id
                        newfeed.save()
                        print('FEED: ' + message.author.name + ' added feed "' + d.feed.title + '" to channel "' + message.channel.name + '" in server "' + message.server.name + '"')
                        await client.send_message(message.channel, "Successfully added " + d.feed.title + "!")
                    else:
                        await client.send_message(message.channel, "Oops! That didn't work! You sure that you gave me a correct feed link?")
                except Exception as err:
                    await client.send_message(message.channel, "Oops! Something went wrong!")
                    raise
            else:
                await client.send_message(message.channel, "Sorry, I can't add feeds in private messages yet!")

        # Remove feed from the current channel
        elif args[1] == "remove":
            if not perms.manage_channels:
                return
            if not len(args[2]) > 0:
                return
            feeds = Feed.select().where(Feed.server == message.server.id and Feed.channel == message.channel.id and Feed.url == args[2])
            if len(feeds) > 0:
                for feed in feeds:
                    feed.delete_instance()
                    print('FEED: ' + message.author.name + ' removed feed ' + feed.url + ' from channel "' + message.channel.name + '" in server "' + message.server.name + '"')
                await client.send_message(message.channel, "Successfully removed feed.")
            else:
                await client.send_message(message.channel, "Feed not found.")

        # List all feeds in the current channel
        elif args[1] == "list":
            feeds = Feed.select().where(Feed.server == message.server.id and Feed.channel == message.channel.id)
            if len(feeds) > 0:
                msg = "**Feeds in this channel:**\n"
                for feed in feeds:
                    msg += "*" + feed.url + "*\n"
                await client.send_message(message.channel, msg)
            else:
                await client.send_message(message.channel, "There are no feeds in this channel!")
