import os

import discord
import requests
from dotenv import load_dotenv
from requests import JSONDecodeError
from datetime import datetime

from django.conf import settings

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'nekomon.settings'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
NEKOMON_API_URL = ""

if settings.DEBUG:
    NEKOMON_API_URL = "http://localhost:8000/api/"
else:
    NEKOMON_API_URL = "https://www.nekomon.es/api/"
    
print("API URL: " + NEKOMON_API_URL)

client = discord.Client()


@client.event
async def on_ready():
    print("Hola me ensendí")


@client.event
async def on_message(message):
    # Prevent sending messages if the sender is another bot
    if message.author.bot:
        return

    # Prevent infinite recursion
    # if message.author.id == client.user.id:
    #    return

    channel = client.get_channel(message.channel.id)
    content = message.content.lower()

    # Posts
    if "nekomon.es/posts/" in content:
        post = content.split("/")
        post = post[len(post) - 1]
        
        print("POST ID: " + post)

        await show_post(channel, post)
        
    # Users
    elif "nekomon.es/" in content:
        username = content.split("/")
        username = username[len(username) - 1]

        await show_user(channel, username)


def get_json_data(api):
    response = ""
    
    try:
        response = requests.get(url=api).json()
    except JSONDecodeError:
        response = None
    finally:
        return response


async def show_post(channel, post):
    loading = await channel.send("Looking for post...")
    
    api_url = NEKOMON_API_URL + "post/" + post
    
    response = get_json_data(api_url)
    
    post = response.get("post")

    if not post:
        await loading.edit(content="The post was not found.")
        return

    id_post = post.get("id")
    content = post.get("content")
    image = post.get("image")
    username = post.get("username")
    profile_picture = post.get("profile_picture")
    created_at = post.get("created_at")
    
    url = "https://www.nekomon.es/posts/" + str(id_post)

    embed = discord.Embed(
        title=(username + " - Nekomon.es"),
        url=url,
        description=content,
        color=discord.Color.orange())
    #embed.set_author(name="Rufinius", url="https://www.twitter.com/MajinTheHandKai",
                     #icon_url="https://www.nekomon.es/web/images/profile_pictures/" + profile_picture)
    #embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
    
    if image != "":
        embed.set_image(url="https://i.imgur.com/" + image + ".jpg")
        
    embed.set_thumbnail(url=("https://i.imgur.com/" + profile_picture + ".jpg"))
    embed.add_field(name="*Date*", value=created_at, inline=False)

    await loading.delete()
    await channel.send(embed=embed)


async def show_user(channel, username):
    loading = await channel.send("Looking for user...")
    
    api_url = NEKOMON_API_URL + "user/" + username
    
    response = get_json_data(api_url)
    
    user = response.get("user")

    if not user:
        await loading.edit(content="The user was not found.")
        return

    username = user.get("username")
    profile_picture = user.get("profile_picture")
    name = user.get("name")
    description = user.get("description")
    date_joined = user.get("date_joined")
    
    url = "https://www.nekomon.es/" + username

    embed = discord.Embed(
        title=(username + " - Nekomon.es"),
        url=url,
        description=description,
        color=discord.Color.orange())
    #embed.set_author(name="Rufinius", url="https://www.twitter.com/MajinTheHandKai",
                     #icon_url="https://www.nekomon.es/web/images/profile_pictures/" + profile_picture)
    #embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=("https://i.imgur.com/" + profile_picture + ".jpg"))
    embed.add_field(name="*Name*", value=name, inline=False)
    embed.add_field(name="*Date joined*", value=date_joined, inline=False)

    await loading.delete()
    await channel.send(embed=embed)

client.run(TOKEN)
