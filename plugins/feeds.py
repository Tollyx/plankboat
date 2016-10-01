import asyncio
import requests
import feedparser
import time
import peewee
import database
import re
import plankboat

sleeptime = 60*15


db = database.getDB()
lastupdate = None

class Feed(database.BaseModel):
    url = peewee.CharField()
    channel = peewee.CharField()
    server = peewee.CharField()
    etag = peewee.CharField()
    modified = peewee.CharField()

async def on_load(client):
    lastupdate = time.gmtime()
    await client.wait_until_ready()

    # feed update loop
    while not client.is_closed:
        for feed, channels in feeds.items():
            d = feedparser.parse(feed.url, etag=feed.etag, modified=feed.modified)
            if d.status == 200:
                feed.etag = d.etag
                feed.modified = d.modified
                feed.save()
                for entry in d.entries:
                    upd = entry.Get('published_parsed', entry.Get('updated_parsed', False))
                    if not upd: return

                    if upd > lastupdate:
                        msg = '**' + d.feed.title + '**\n*' + entry.title + '*\n' + entry.link
                        server = discord.utils.find(lambda s: s.id == feed.server, client.servers)
                        if server:
                            channel = discord.utils.find(lambda c: c.id == feed.channel, server.channels)
                            if channel:
                                client.send_message(channel, msg)
        lastupdate = time.gmtime()
        await asyncio.sleep(sleeptime)

feedre = re.compile(r"\s*feed\s+(\S+)\s+(\S+)")

async def on_message(client, message):
    # return if the message doesn't start with a mention
    prefix = client.user.mention
    msg = message.content
    if not msg.startswith(prefix): return

    msg = msg[len(prefix):]

    match = feedre.match(msg)
    if match:
        if match.group(1) == "add":
            if not message.channel.is_private:
                try:
                    d = feedparser.parse(match.group(2))
                    if d == 200:
                        newfeed = Feed()
                        newfeed.url = match.group(2)
                        newfeed.etag = d.etag
                        newfeed.modified = d.modified
                        newfeed.channel = message.channel.id
                        newfeed.save()
                except Exception as e:
                    raise
            else:
                client.send_message(message.channel, "Sorry, I can't add feeds to PMs yet!")


