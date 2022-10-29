# imports discord library
import discord

# Creates a 'Client.' Clients are the connection between the code and discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Registers an event
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message): # On Message happens everytime a message is sent
    if message.author == client.user: # This returns if the message is sent by the bot
        return

    if message.content.startswith('$hello'): #if the message starts w "$hello" the bot will reply "Hello!"
        await message.channel.send('blake its me ur father, i want to tell you something (reply "$what" to find out what your father wants to tell you')

    if message.content.startswith('$what'):
        await message.channel.send('ur gay')


    embedT = discord.Embed(
        title='GUYS CHECK THIS OUT',
        description='this is the coolest SHIT ive ever seen',
        url='https://youtu.be/S9uTScSgzrM',
        color=discord.Color.teal(),


    )

    if message.content.startswith('$embed'):
        await message.channel.send(embed=embedT)


with open("token", "r") as fd:
    client.run(fd.read())