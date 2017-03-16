import json
import os

import discord

# Commands #
from commands.prog import prog
from commands.mythic import mythic
from commands.kills import kills

CLIENT = discord.Client()


def config_value(key):
    with open(os.path.join(os.path.dirname(__file__), 'config.json')) as config_file:
        config = json.load(config_file)

    try:
        value = os.environ[key.upper()]
    except KeyError:
        value = config.get(key)
    return value


@CLIENT.event
async def on_ready():
    print('Logged in as')
    print(CLIENT.user.name)
    print(CLIENT.user.id)
    print('------')


@CLIENT.event
async def on_message(message):

    if message.content.startswith('!info') or message.content.startswith('!help'):
        await CLIENT.send_message(message.channel, 
                        "I'm PugBot, the pug checker!\n"
                        "Available commands are:"
                        "     ?prog (for bosses killed across all expansion raids and difficulties)"
                        "     ?mythic (for seeing how many successful Mythic+ dungeons have been completed across which difficulties)"
                        "     ?kills (for seeing how many times each boss has been killed in highest difficult completed)"
                        "Use: <command> <name> <server>\n"
                        "Example: !prog Cornelious Area-52")

    if message.content.startswith('?prog'):
        await prog(CLIENT, DEFAULT_REGION, BLIZZARD_API_KEY, message)
        
    if message.content.startswith('?mythic'):
        await mythic(CLIENT, DEFAULT_REGION, BLIZZARD_API_KEY, message)
        
    if message.content.startswith('?kills'):
        await kills(CLIENT, DEFAULT_REGION, BLIZZARD_API_KEY, message)


if __name__ == '__main__':
    BLIZZARD_API_KEY = config_value('blizzard_api_key')
    DEFAULT_REGION = config_value('default_region')
    DISCORD_TOKEN = config_value('discord_token')
    CLIENT.run(DISCORD_TOKEN)
