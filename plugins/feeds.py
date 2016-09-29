import asyncio
import requests
import feedparser
import time

lastupdate = None
feeds = {}

async def on_load(client):
    lastupdate = time.gmtime()
    await client.wait_until_ready()

    # feed update loop
    while not client.is_closed:
        for feed, channels in feeds.items():
            d = feedparser.parse(feed)
            for entry in d.entries:
                if entry.published > lastupdate:
                    msg = '**' + d.feed.title + '**\n*' + entry.title + '*\n' + entry.link
                    for channel in channels:
                        client.send_message(channel, msg)
        lastupdate = time.gmtime()
        await asyncio.sleep(60 * 15)

async def on_message(client, message):
    pass