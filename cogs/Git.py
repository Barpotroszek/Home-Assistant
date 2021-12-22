from discord.ext.commands import Cog, command
from subprocess import run

class Git(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="git")
    async def git_command_handler(self, ctx, *args):
        '''Obsługa gita w kontenerze/Bocie'''
        if args == ():
            args = ("status",)
        cmd = ['git']+[a for a in args]
        proc = run(cmd, shell=True, text=True, capture_output=True)
        await ctx.send(f"```sh\n{proc.stdout}```")

def setup(bot):
    bot.add_cog(Git(bot))        