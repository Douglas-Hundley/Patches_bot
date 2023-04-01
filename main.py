import disnake
import aiohttp
import time
import openai
from random import random, randrange
from disnake import Member, Color
from disnake.ext import commands
from config import BOT_TOKEN, SERVER_TOKEN, CHAT_GPT_TOKEN


client = commands.Bot(command_prefix="!",
                      intents=disnake.Intents.all())


openai.api_key = CHAT_GPT_TOKEN


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')
        print("test")

    # Generate a response using the OpenAI API
    if message.content.startswith("!chatgpt"):
        prompt = f"{message.content}\n\nAI:"
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

    # Send the generated text as a message in the channel
        await message.channel.send(generated_text)
    # changes user role
    if message.content.startswith("!changerole"):
        # Get the role to change to
        role_name = message.content.split()[1]
        role = disnake.utils.get(message.guild.roles, name=role_name)

        # Change the user's role
        await message.author.add_roles(role)
        await message.channel.send(f"{message.author.mention}, your role has been changed to {role_name}.")

    if message.content.startswith("!changecolor"):
        hex_color = message.content.split()[1]
        print(hex_color)
        # Convert the hex color code to RGB
        rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        # Get the user's roles and find the top role
        member: Member = message.guild.get_member(message.author.id)
        roles = member.roles
        top_role = member.top_role

        # Modify the top role's color and update the user's roles
        new_color = Color.from_rgb(*rgb_color)
        await top_role.edit(color=new_color)
        await member.edit(roles=roles)

        await message.channel.send(f"{message.author.mention}, your color has been changed to {hex_color}.")

        # generates random number 1 through 6
    if message.content.startswith("!roll d6"):
        await message.channel.send(randrange(1, 6))

        # generates random number 1 through 20
    if message.content.startswith("!roll d20"):
        await message.channel.send(randrange(1, 20))

        # starts stopwatch for channel
    if message.content.startswith("!stopwatch"):
        time = message.content.split()[1]
        time.sleep(time)
        await message.channel.send("Time is up!")

client.run(BOT_TOKEN)
