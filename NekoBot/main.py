import os

import discord
import requests
from dotenv import load_dotenv
from requests import JSONDecodeError
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
NEKOMON_USER_URL = os.getenv('NEKOMON_USER_URL')

client = discord.Client()


@client.event
async def on_ready():
    print("Hola me ensendí")


@client.event
async def on_message(message):
    # Prevent sending messages if the the sender is another bot
    if message.author.bot:
        return

    # Prevent infinite recursion
    #if message.author.id == client.user.id:
    #    return

    channel = client.get_channel(message.channel.id)
    content = message.content

    if content.startswith("/user "):
        username = content.split(" ")[1]

        await show_user(channel, username)


def get_json_data(api):
    response = ""

    try:
        response = requests.get(url=api).json()
    except JSONDecodeError:
        response = False
    finally:
        return response


async def show_user(channel, username):
    response = get_json_data(NEKOMON_USER_URL + username)

    user = response.get("user")[0]

    if not user:
        await channel.send("The username was not found")
        return

    user_data = user.get("fields")

    username = user_data.get("username")
    profile_picture = user_data.get("profile_picture")
    name = user_data.get("name")
    description = user_data.get("description")
    #date_joined = datetime.strptime(user_data.get("date_joined"), '%d/%m/%y')
    date_joined = user_data.get("date_joined")
    #datetime.strftime(user_data.get("date_joined", "%d/%m/%y")) + ""

    #"Information of the username " + username + " on Nekomon.es"

    embed = discord.Embed(
        title=(username + " - Nekomon.es"),
        url="https://www.nekomon.es/Rufino",
        description=description,
        color=discord.Color.blue())
    #embed.set_author(name="Rufinius", url="https://www.twitter.com/MajinTheHandKai",
                     #icon_url="https://www.nekomon.es/web/images/profile_pictures/"+profile_picture)
    # embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=("https://www.nekomon.es/web/images/profile_pictures/" + profile_picture))
    embed.add_field(name="*Name*", value=name, inline=False)
    embed.add_field(name="*Date joined*", value=date_joined, inline=False)

    await channel.send(embed=embed)


client.run(TOKEN)
