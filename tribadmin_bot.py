import discord
import os
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
    async def on_ready():
        print(f'The bot has successfully connected!')

    @client.event
    async def on_member_join(member):
        await member.send(f'Welcome to the TRIB Discord server, {member.name}, please look around!')

    @client.event
    async def on_message(message):
        if 'admin' in [role.name for role in message.author.roles]:
            if message.author == client.user:
                return
            term = message.content.lstrip(CMD_PREFIX)
            if term in msgs:
                response = msgs[term]
                await message.channel.send(response)
            elif message.content.startswith('!'):
                await message.channel.send("I don't understand that command.")
            elif message.content == 'raise-exception':
                raise discord.DiscordException

    try:
        client.run(TOKEN)
    except Exception as e:
        print(f'Error when logging in: {e}')


if __name__ == "__main__":
    main()
