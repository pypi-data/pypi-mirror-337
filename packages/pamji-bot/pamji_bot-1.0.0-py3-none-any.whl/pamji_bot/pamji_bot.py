# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import os
import discord
import requests
import json
import logging
import hmac
import os
import subprocess
from pathlib import Path
from ai_api_utils import generate_deepseek_text
from ai_api_utils import generate_gemini_text
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_TOKENS = int(os.getenv("MAX_TOKENS", "256"))
intents = discord.Intents.default()
intents.message_content = True
discord_client = discord.Client(intents=intents)


async def send_response(channel, response):
  for guild in discord_client.guilds:
            channel = discord.utils.get(guild.text_channels, name=channel)
            if channel:
                try:
                    await channel.send(response)
                except requests.exceptions.RequestException as e:
                    await channel.send(
                        f"Error: {e}")
                except KeyError:
                    await channel.send(
                        "Error: Channel not found."
                    )
async def send_response2(guild, channel_name, response, autor, id, member_id):
    """Sendet die Antwort nur im angegebenen Server (guild)"""
    channel = discord.utils.get(guild.text_channels, name=channel_name)
    if channel:
        chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
        for chunk in chunks:
            await channel.send(chunk)
    else:
        # Fallback: Wenn der Kanal nicht existiert, im aktuellen Channel antworten
        for guild_channel in guild.text_channels:
            if guild_channel.permissions_for(guild.me).send_messages:
                chunks = [f"⚠️ Kanal '{channel_name}' nicht gefunden! Hier ist die Antwort:\n{response[i:i+1900]}" for i in range(0, len(response), 1900)]
                for chunk in chunks:
                    await guild_channel.send(chunk)
                break

@discord_client.event
async def on_ready():
    logger.info('We have logged in as {0.user}'.format(discord_client))
    # Greeting message disabled to avoid spam
    await send_response('bot-talk', 'Hello! How can I help you today?')


async def close_bot():
    for guild in discord_client.guilds:
        channel = discord.utils.get(guild.text_channels, name='bot-talk')
        if channel:
            await channel.send("Goodbye everyone! Bot is going offline.")
    await discord_client.close()


@discord_client.event
async def on_message(message):
    author = message.author.global_name
    member_id = message.author.id
    guild = message.guild
    id = message.id
    channel = message.channel.name
    logger.info(f"Message received: {message.content}")
    if message.author == discord_client.user:
        return
    if message.content.startswith('$hello'):
        logger.info("hello command invoked")
        await send_response('bot-talk', 'Hello! How can I help you today?')
    if message.content.startswith('$shutdown'):
        await close_bot()
    if message.content.startswith('gemini'):
        logger.info("gemini command invoked")
        user_input = message.content[len('gemini '):]
        response = generate_gemini_text(user_input)
        await send_response2(guild, channel, response, author, id, member_id)
    if message.content.startswith('$deepseek'):
        logger.info("deepseek command invoked")
        user_input = message.content[len('$deepseek '):]
        response = generate_deepseek_text(user_input)
        await send_response('bot-talk', response)

def start_bot():
    try:
        token = os.getenv("DISCORD_TOKEN") or ""
        if token == "":
            raise Exception("Please add your token to the Secrets pane.")
        discord_client.run(token)
    except discord.HTTPException as e:
        if e.status == 429:
            logger.error("The Discord servers denied the connection for making too many requests")
            logger.error("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
        else:
            raise e

if __name__ == '__main__':
    start_bot()