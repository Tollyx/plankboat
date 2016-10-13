import asyncio
import requests
import re

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
    headers = {'Accept-Encoding': 'identity'}

    if command == '^movie' or '^tv' or '^actor':
        url = 'http://www.imdb.com/find?ref_=nv_sr_fn&q='+args.replace(' ', '+')
        if url is not None:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                if command == '^movie' or command == '^tv':
                    imdb = re.search('/title/(.+?)/?ref_=fn_al_tt_1', response.text)
                elif command == '^actor':
                    imdb = re.search('/name/(.+?)/?ref_=fn_al_nm_1', response.text)
                    
                imdbID = imdb.group(1)
#DEBUG          print(str(imdbID))

                if command == '^movie' or command == '^tv':
                    url = 'http://www.imdb.com/title/' + imdbID
                    if url is not None:
                        page = requests.get(url)
                        if page.status_code == 200:         
                            info = re.search('"description">(.*?)</', page.text, re.DOTALL)
                            description = str(info.group(1))
                            result = url + '\nDescription: ' + description

                elif command == '^actor':
                    url = 'http://www.imdb.com/name/' + imdbID
                    result = url
                    
                await client.send_message(message.channel, result)
            elif response.status_code == 204:
                await client.send_message(message.channel, "Sorry, didn't find anything!")
            else:
                print('IMDB:', 'Error code: '+str(response.status_code))