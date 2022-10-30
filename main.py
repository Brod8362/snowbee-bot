import discord
import snowbee_api

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

VENDORS = dict(map(lambda x: (x.id, x), snowbee_api.fetch_vendors()))
GLOBAL_EMBED_TABLE: dict = {}

EMOJI_ARROW_LEFT = "⬅️"
EMOJI_ARROW_RIGHT = "➡️"


def build_embed(product: snowbee_api.Product):
    embed_obj: discord.Embed = discord.Embed(
        title=product.name,
        color=discord.Color.teal(),
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


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message: discord.Message):  # Reads every message sent

    if message.author == client.user or message.author.bot:  # Returns instantly if message is sent by the bot
        return

    if message.content.startswith('$search'):  # User Searches for objects and Bot Generates Embed function with result
        await command_search(message)


@client.event
async def on_reaction_remove(reaction: discord.Reaction, _user: discord.Member):
    await handle_embed_page(reaction)


@client.event
async def on_reaction_add(reaction: discord.Reaction, _user: discord.Member):
    await handle_embed_page(reaction)


async def handle_embed_page(reaction: discord.Reaction):
    if reaction.message.id in GLOBAL_EMBED_TABLE:
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
                return  # abort, this index is out of boudns

            embed_state["index"] = new_index
            await reaction.message.edit(embed=embed_state["embeds"][new_index])


# Allows Discord bot to communicate with Program using Token
if __name__ == "__main__":
    with open("token", "r") as fd:
        client.run(fd.read())
