import os
import disnake
import aiohttp
import time
import openai
from random import random, randrange
from disnake import Member, Color
from disnake.ext import commands
#from config import BOT_TOKEN, SERVER_TOKEN, CHAT_GPT_TOKEN


bot = commands.Bot(command_prefix='!',
                   intents=disnake.Intents.all(), help_command=None)

openai.api_key = os.environ['CHAT_GPT_TOKEN']


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command(name='help')
async def help_command(ctx):
    embed = disnake.Embed(title="Bot Commands", color=0x00ff00)
    embed.add_field(name="!hello", value="Say hello to the bot", inline=False)
    embed.add_field(
        name="!chatgpt", value="Generate a response using the OpenAI API", inline=False)
    embed.add_field(name="!changerole <role_name>",
                    value="Change the user's role", inline=False)
    embed.add_field(name="!changecolor <hex_color>",
                    value="Change the user's color", inline=False)
    embed.add_field(name="!roll d6",
                    value="Generate a random number from 1 to 6", inline=False)
    embed.add_field(
        name="!roll d20", value="Generate a random number from 1 to 20", inline=False)
    embed.add_field(name="!stopwatch <seconds>",
                    value="Start a stopwatch for the specified number of seconds", inline=False)

    await ctx.send(embed=embed)


@bot.command(name="chatgpt")
async def chat(ctx):
    prompt = f"{ctx.message.content}\n\nAI:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
        best_of=1,
    )
    generated_text = response.choices[0].text.strip()
    await ctx.send(generated_text)


# @bot.command(name="changerole")
# async def role(ctx):
#     # Get the role to change to
#     role_name = ctx.message.content.split()[1]
#     role = disnake.utils.get(ctx.guild.roles, name=role_name)

#     # Change the user's role
#     await ctx.author.add_roles(role)
#     await ctx.send(f"{ctx.author.mention}, your role has been changed to {role_name}.")


@bot.command(name="changecolor")
async def color(ctx):
    hex_color = ctx.message.content.split()[1]
    # Convert the hex color code to RGB
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # Get the user's roles and find the top role
    member: Member = ctx.guild.get_member(ctx.author.id)
    roles = member.roles
    top_role = member.top_role

    # Modify the top role's color and update the user's roles
    new_color = Color.from_rgb(*rgb_color)
    await top_role.edit(color=new_color)
    await member.edit(roles=roles)

    await ctx.send(f"{ctx.author.mention}, your color has been changed to {hex_color}.")


@bot.command(name="roll")
async def roll(ctx, dice: str):
    if dice == "d6":
        await ctx.send(randrange(1, 7))
    elif dice == "d20":
        await ctx.send(randrange(1, 21))
    else:
        await ctx.send("Invalid dice type. Please choose either d6 or d20.")


bot.run(os.environ['BOT_TOKEN'])
