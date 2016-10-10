import re
import requests
import asyncio
import xml.etree.ElementTree as ET

# MyAnimeList requires a login to use their API
mal_username = 'username'
mal_password = 'password'

async def on_command(client, message, args):
    if not args[0] in ['anime', 'manga']: return

    url = 'https://myanimelist.net/api/' + args[0] + '/search.xml?q='+'+'.join(args[1:])

    if url is not None:
        response = requests.get(url, auth=(mal_username,mal_password))
        if response.status_code == 200:
            anime = ET.fromstring(response.text)

            result = '***' + anime[0].findtext('title') + '***\n'
            engname = anime[0].findtext('english')

            if len(engname) > 0:
                result += '*(' + engname + ')*\n'

            result += '\n' + anime[0].findtext('synopsis') + '\n'

            result += '**score:** ' + anime[0].findtext('score') + '\n'
            result += '**status:** ' + anime[0].findtext('status') + '\n'

            if args[0] == 'manga':
                result += '**chapters:** ' + anime[0].findtext('chapters') + '\n'
                result += '**volumes:** ' + anime[0].findtext('volumes') + '\n'
            elif args[0] == 'anime':
                result += '**episodes:** ' + anime[0].findtext('episodes') + '\n'

            result += 'https://myanimelist.net/' + args[0] + '/'+anime[0].findtext('id') + '/'

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
            await client.send_message(message.channel, "Sorry, didn't find anything!")
        else:
            print('MAL:', 'Error code: '+str(response.status_code))