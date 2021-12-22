from discord.ext.commands import Cog, command
from subprocess import run

class Git(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="git", usage="<option>", help="Sterowanie gitem")
    async def git(self, ctx, *args):
        if len(args)==0:
            cmd = ['git', "status"]
        else:
            cmd = ['git']+[a for a in args]
        proc = run(" ".join(cmd), shell=True, text=True, capture_output=True)
        if proc.returncode == 0:
            await ctx.send(f"Output:\n```\n{proc.stdout}```")
        else:
            await ctx.send(f"Error:\n```\n{proc.stderr}```")

def setup(bot):
    bot.add_cog(Git(bot))        