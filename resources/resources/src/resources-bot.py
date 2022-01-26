# resources-bot
from heapq import nsmallest
import os
from pprint import pformat

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from resources.resources import get_current_csv, GHServer

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)
client = discord.Client()

## Configurations

# channel names that this bot will send to
allowed_channel_names = [
    'resources-bot'
]

## End configurations

def get_compatible_channels():
    channel_ids = []
    for guild in client.guilds:
        print(f'found guild: {guild.name}')
        for channel in guild.channels:
            print(f'found channel: {channel.name}')
            if channel.name in allowed_channel_names:
                channel_ids.append(channel.id)
    return channel_ids

@tasks.loop(minutes=15)
async def called_once_an_hour():
    channel_ids = get_compatible_channels()
    for channel_id in channel_ids:
        channel = client.get_channel(channel_id)
        # await channel.send('test')

        print('getting new data')
        new_rows = get_current_csv()
        num_new_rows = len(new_rows)
        print(f'{num_new_rows} new resources')
        for n in new_rows:

            # remove things useless to a human
            n.pop('galaxy_id')
            n.pop('type_id')
            n.pop('group_id')

            # reformat some things

            # make name a hyper link to GH
            n['link'] = f'https://galaxyharvester.net/resource.py/{GHServer.FINALIZER.value}/{n["name"]}'

            # Endor|Yavin 4 -> Endor, Yavin4
            n['planets'] = ','.join(n['planets'].split('|')) 

            n_str = '\n'.join([f'{k}: {v}' for k,v in n.items()])
            print(n_str)
            await channel.send(f'**A new resource has been verified on Galaxy Harvestor:**\n{n_str}')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        print(f'In guild: {guild.name}')
    

called_once_an_hour.start()

client.run(TOKEN)