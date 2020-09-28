import discord
import os
from dotenv import load_dotenv
from util.csv_url import JsonGetter
from help_page import HelpCreate

# Globals.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CONTENT = os.getenv('TRIB_CONTENT_JSON')
CMD_PREFIX = os.getenv('CMD_PREFIX')


def check_roles(disc_roles, roles=('mentor', 'core', 'admin')):
    """
    Check the list of roles to see if you can run the command.
    Add discord_roles = [role.name for role in message.author.roles] to get list of all user roles.
    :return:
    """
    for role in roles:
        if role in disc_roles:
            return True
    return False


def main():

    client = discord.Client()
    msgs = JsonGetter(CONTENT)

    @client.event
    async def on_ready():
        print(f'The bot has successfully connected!')

    @client.event
    async def on_member_join(member):
        await member.send(f'Welcome to the TRIB Discord server, {member.name}, please look around!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        term = message.content.lstrip(CMD_PREFIX)
        if term.lower() in msgs.data:
            response = msgs.data[term]
            await message.channel.send(response)
        elif term == 'entries':
            response = HelpCreate(msgs.entries, cmd_char=CMD_PREFIX).final_entries
            for resp in response:
                await message.author.send(resp)
        elif term == 'help':
            response = HelpCreate(msgs.entries).final_help
            for resp in response:
                await message.author.send(resp)
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
