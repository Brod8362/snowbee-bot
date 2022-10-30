import discord
import requests

# Creates a 'Client.' Clients are the connection between the code and discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

r = requests.get('http://api.snowbee.byakuren.pw/info')
json = r.json()
json["version"]

def build_embed(tosearch):
    embedObj = discord.Embed(
        title=tosearch,
        color=discord.Color.teal()
    )
    embedObj.add_field(name='Price:', value='One Billion Dollars', inline=False)
    embedObj.add_field(name='Seller:', value='Blake Rodriguez', inline=False)
    embedObj.add_field(name='Rating:', value='11/10', inline=False)

    return embedObj

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):  # Reads every message sent

    if message.author == client.user:   # Returns instantly if message is sent by the bot
        return

    if message.content.startswith('$search'):
        tosearch = message.content[8:]
        await message.channel.send('Searching for "' + tosearch + '"')
        await message.channel.send(embed=build_embed(tosearch))




with open("token", "r") as fd:
    client.run(fd.read())