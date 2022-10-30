import discord
import snowbee_api

#   Creates Client for bot to use in discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

VENDORS = dict(map(lambda x: (x.id, x), snowbee_api.fetch_vendors()))
GLOBAL_EMBED_TABLE: dict = {}

# Variables because the arrow emojis are illegible in pycharm lol
EMOJI_ARROW_LEFT = "⬅️"
EMOJI_ARROW_RIGHT = "➡️"

#   Function to build the Embed from the information from the API
def build_embed(product: snowbee_api.Product):
    embed_obj: discord.Embed = discord.Embed(
        title=product.name,
        color=discord.Color.from_rgb(118, 219, 233),
        url=product.product_page
    )
    embed_obj.set_thumbnail(url=product.preview_url)
    embed_obj.add_field(name="Price", value=f"${product.price:.2f}", inline=False)
    vendor: snowbee_api.Vendor = VENDORS.get(product.vendor_id, None)
    if vendor is not None:
        embed_obj.set_footer(text=vendor.name, icon_url=vendor.favicon)

    return embed_obj


async def command_search(context: discord.Message):
    args: list[str] = context.content.split(" ")
    query: str = " ".join(args[1:])
    if not query:
        await context.reply("Try inputting a query and try again.")
        return
    try:
        products = snowbee_api.fetch_products(query)
        if len(products) == 0:
            await context.reply(f"No results found for **{query}**.")
        else:
            product_embeds = list(map(build_embed, products))
            bot_msg: discord.Message = await context.reply(embed=product_embeds[0])
            GLOBAL_EMBED_TABLE[bot_msg.id] = {
                "index": 0,
                "embeds": product_embeds
            }
            await bot_msg.add_reaction(EMOJI_ARROW_LEFT)
            await bot_msg.add_reaction(EMOJI_ARROW_RIGHT)
    except RuntimeError:
        await context.reply("Sorry, there was an error performing your request.")

#   Scrolls between search results inside one Embed using the reaction arrows
async def handle_embed_page(reaction: discord.Reaction, user: discord.Member):
    if not user.bot and reaction.message.id in GLOBAL_EMBED_TABLE:
        embed_state: dict = GLOBAL_EMBED_TABLE[reaction.message.id]
        if reaction.emoji == EMOJI_ARROW_LEFT:
            direction = -1
        elif reaction.emoji == EMOJI_ARROW_RIGHT:
            direction = 1
        else:
            return
        if direction != 0:
            new_index = embed_state["index"] + direction
            if new_index < 0 or new_index >= len(embed_state["embeds"]):
                return  # abort, this index is out of bounds

            embed_state["index"] = new_index
            await reaction.message.edit(embed=embed_state["embeds"][new_index])

@client.event
async def on_ready(): # Sends a message in console when bot activates
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message: discord.Message):  # Reads every message sent

    if message.author.bot:  # Returns instantly if message is sent by the bot
        return

    if message.content.startswith('$search'):  # User Searches for objects and Bot Generates Embed function with result
        await command_search(message)


#   Reaction Arrow Events
@client.event
async def on_reaction_remove(reaction: discord.Reaction, user: discord.Member):
    await handle_embed_page(reaction, user)

@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.Member):
    await handle_embed_page(reaction, user)


# Allows Discord bot to communicate with Program using Token
if __name__ == "__main__":
    with open("token", "r") as fd:
        client.run(fd.read())
