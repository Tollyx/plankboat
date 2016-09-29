import re
import requests
import asyncio
import xml.etree.ElementTree as ET

# MyAnimeList requires a login to use their API
mal_username = 'username'
mal_password = 'password'

async def on_message(client, message):
    prefix = client.user.mention
    msg = message.content
    if not msg.startswith(prefix): return
    msg = msg[len(prefix):]
    match = re.match(r"^\s*(\w*)", msg)
    if not match: return

    command = match.group(1)
    args = msg[len(command)+2:]
    url = None
    if command == "anime":
        url = 'https://myanimelist.net/api/anime/search.xml?q='+args.replace(' ','+')
    elif command == "manga":
        url = 'https://myanimelist.net/api/manga/search.xml?q='+args.replace(' ','+')

    if url is not None:
        #print('MAL:', url)
        response = requests.get(url, auth=(mal_username,mal_password))
        if response.status_code == 200:
            anime = ET.fromstring(response.text)
            #print('MAL:', 'Found: '+str(len(anime)))
            result = '***' + anime[0].findtext('title') + '***\n'
            engname = anime[0].findtext('english')

            if len(engname) > 0:
                result += '*(' + engname + ')*\n'

            result += '\n' + anime[0].findtext('synopsis') + '\n'

            result += '**score:** ' + anime[0].findtext('score') + '\n'
            result += '**status:** ' + anime[0].findtext('status') + '\n'

            if command == 'manga':
                result += '**chapters:** ' + anime[0].findtext('chapters') + '\n'
                result += '**volumes:** ' + anime[0].findtext('volumes') + '\n'
            elif command == 'anime':
                result += '**episodes:** ' + anime[0].findtext('episodes') + '\n'

            result += 'https://myanimelist.net/'+command+'/'+anime[0].findtext('id') + '/'

            # Oh dear god these formatting thingies are killing me
            result = result.replace('<br />', '\n')
            result = result.replace('[i]','*')
            result = result.replace('[/i]','*')
            result = result.replace('[b]','**')
            result = result.replace('[/b]','**')
            result = result.replace('&quot;', '"')
            result = result.replace('&#039;', "'")
            result = result.replace('&mdash;', "—")
            result = re.sub('\n\n+', '\n\n', result)

            await client.send_message(message.channel, result)
        elif response.status_code == 204:
            #print('MAL:', 'Found nothing.')
            await client.send_message(message.channel, "Sorry, didn't find anything!")
        else:
            print('MAL:', 'Error code: '+str(response.status_code))