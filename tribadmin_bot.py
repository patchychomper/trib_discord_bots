import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from util.csv_url import CsvGetter


# Globals.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CONTENT = os.getenv('TRIB_CONTENT')
CMD_PREFIX = os.getenv('CMD_PREFIX')


def main():

    client = discord.Client()
    msgs = CsvGetter(CONTENT).data

    @client.event
    @commands.has_role('admin')
    async def on_message(message):
        if message.author == client.user:
            return
        term = message.content.lstrip(CMD_PREFIX)
        if term in msgs:
            response = msgs[term]
            await message.channel.send(response)
        elif message.content == 'raise-exception':
            raise discord.DiscordException
        elif message.content.startswith('!'):
            await message.channel.send("I don't understand that command.")

    try:
        client.run(TOKEN)
    except Exception as e:
        print(f'Error when logging in: {e}')


if __name__ == "__main__":
    main()
