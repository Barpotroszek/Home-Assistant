from os import chdir, system
from os.path import dirname

system("cls")
chdir(dirname(__file__))

from config.config import TOKEN, __cogs__, startup
from discord import Embed
from discord.ext import commands
from discord.ext.commands.errors import NoEntryPointError

bot = commands.Bot(command_prefix=">", description="Nadzorca domu")

@bot.event
async def on_connect():
    await startup(bot)
    print("Bot połączył się z Discordem.\nWczytywanie danych...")
    for cog in __cogs__():
        try:
            bot.load_extension(cog)
        except NoEntryPointError:
            print(f" -> Cog {cog} nie ma funkcji *setup*")
        except Exception as e:
            print(f"{cog} -> {e}")
             
    print("Dane wczytane")


@bot.event
async def on_ready():
    print("\nZalogowano jako:", bot.user)
    print("----------------------------------")

@bot.command()
async def reload(ctx):
    """Reload all cogs"""
    system('cls')
    await startup(bot)
    #settings = _json(CONFIG_FILE_PATH).read()
    async with ctx.typing():
        embed = Embed(
            title="Reloading cogs",
            color=0xb06a09,
            timestamp=ctx.message.created_at
        )
        print(__cogs__())
        for cog in __cogs__():
            try:
                bot.unload_extension(cog)
                bot.load_extension(cog)
                embed.add_field(
                    name=cog,
                    value="Reloaded",
                    inline=False
                )
            except Exception:
                try:
                    bot.add_cog(cog)
                except Exception as e:
                    embed.add_field(
                        name=cog,
                        value=e.args,
                        inline=False
                    )  
    
    msg = await ctx.send(embed=embed)
    await ctx.message.delete(delay=5)
    await msg.delete(delay=5)

bot.run(TOKEN)
