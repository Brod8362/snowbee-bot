import discord
import requests

# Creates a 'Client.' Clients are the connection between the code and discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def build_embed(product: dict):
    embedObj = discord.Embed(
        title=product["name"],
        color=discord.Color.teal()
    )
    embedObj.add_field(name='Price:', value=f"${product['price']}", inline=False)
    embedObj.add_field(name='Vendor:', value=product["vendor"], inline=False)
    embedObj.add_field(name='Rating:', value='11/10', inline=False)

    return embedObj

def search_json(tosearch):
    response = requests.post(
        "http://api.snowbee.byakuren.pw/search",
        json={
            "query": tosearch
        }
    )

    if response.status_code == 404:
        return None
    elif response.status_code == 200:
        return response.json()["products"]

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):  # Reads every message sent

    if message.author == client.user:   # Returns instantly if message is sent by the bot
        return

    if message.content.startswith('$search'):   # User Searches for objects and Bot Generates Embed function with result
        tosearch = message.content[8:]
        products = search_json(tosearch)
        if products is None:
            # nothing
            pass
        else:
            product_embeds = map(build_embed, products)

            await message.channel.send('Searching for "' + tosearch + '"')
            await message.channel.send(embed=build_embed(tosearch))

# Allows Discord bot to communicate with Program using Token
with open("token", "r") as fd:
    client.run(fd.read())