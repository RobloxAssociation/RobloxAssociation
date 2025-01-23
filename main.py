import discord
from discord.ext import commands
import os
from config import TOKEN
import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="r.", intents=intents)

async def load_commands():
    for root, _, files in os.walk('./cogs'):
        for file in files:
            if file.endswith('.py') and file != '__init__.py' and file != 'key.py':
                # Converte o caminho do arquivo em um formato de pacote
                path = os.path.join(root, file).replace("\\", "/")
                module = path.replace('./', '').replace('/', '.').replace('.py', '')
                await bot.load_extension(module)

async def load_events():
    for filename in os.listdir('./events'):
        if filename.endswith('.py') and filename != '__init__.py' and filename != 'key.py':
            await bot.load_extension(f"events.{filename[:-3]}")

@bot.event
async def on_ready():
    print(f'{bot.user} está conectado ao Discord!')
    await load_commands()
    await load_events()
    await bot.tree.sync()

    channelId = 1327887076611457044
    botStatus = bot.get_channel(channelId)
    now = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    embed = discord.Embed(title="[RBOA] Bot | Online", description="I' am online now!", colour=discord.Colour.brand_green())
    embed.add_field(name="Online since", value= now)
    embed.set_image(url=bot.user.avatar.url)

    await botStatus.send(embed=embed)

@bot.event
async def on_disconnect():
    channelId = 1327887076611457044
    botStatus = bot.get_channel(channelId)
    now = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    embed = discord.Embed(title="[RBOA] Bot | Offline", description="I' am offline now! D:", colour=discord.Colour.brand_red())
    embed.add_field(name="Offline since", value= now)
    embed.set_image(url=bot.user.avatar.url)

    await botStatus.send(embed=embed)

bot.run(TOKEN) 
