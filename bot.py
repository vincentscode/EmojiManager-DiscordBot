import discord
import aiohttp

from config import Configuration

config = Configuration.load()
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.slash_command(name='emojis', description='List all emojis in the server', guild_ids=config.testing_guild_ids)
async def list_emojis(ctx: discord.ApplicationContext, animated: bool = False):
    emojis = [e for e in ctx.guild.emojis if e.animated == animated]
    num_emojis = len(emojis)

    if num_emojis == 0:
        await ctx.respond('No emojis in this server')
        return

    chunks = [emojis[i:i + 25] for i in range(0, num_emojis, 25)]

    chunk_count = len(chunks)
    chunk_index = 1
    for chunk in chunks:
        title = f'Emojis {chunk_index*25-24}-{min(chunk_index*25, num_emojis)} of {num_emojis}'
        if animated:
            title = 'Animated ' + title

        embed = discord.Embed(title=title)
        embed.set_footer(text=f'Page {chunk_index} of {chunk_count}')
        embed.color = discord.Color.blurple()

        for emoji in chunk:
            embed.add_field(name=emoji.name, value=str(emoji))

        await ctx.respond(embed=embed)
        chunk_index += 1

@bot.slash_command(name='add_emojis', description='Add a bunch of emojis from a tsv file', guild_ids=config.testing_guild_ids)
@discord.default_permissions(administrator=True)
async def add_emojis(ctx: discord.ApplicationContext, file: discord.Attachment):
    await ctx.defer()

    file_content = await file.read()
    emoji_lines = file_content.decode('utf-8').split('\n')

    emojis = []
    for line in emoji_lines:
        if not line:
            continue

        url, name = line.split('\t')
        emojis.append((name, url))

    static_emoji_slots_used = len([e for e in ctx.guild.emojis if not e.animated])
    free_emoji_slots = ctx.guild.emoji_limit - static_emoji_slots_used

    if len(emojis) > free_emoji_slots:
        await ctx.respond(f'Not enough free emoji slots. {free_emoji_slots} slots available')
        return
    
    print(emojis)
    
    for name, url in emojis:
        # normalize name
        name = name.replace(":", "").strip()

        print(f'Adding emoji {name} from {url}')

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                emoji_data = await resp.read()
                emoji = await ctx.guild.create_custom_emoji(name=name, image=emoji_data, reason=f'Added by {ctx.author} using the add_emojis command')
                print(f'Created emoji {emoji.name} with id {emoji.id}')

    await ctx.followup('Emojis added')

bot.run(config.token)
