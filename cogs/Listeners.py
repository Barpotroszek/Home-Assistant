from discord.ext.commands import Cog
from config.config import settings, StatusMessage

choinka_id = 14
choinka_switch_id = 4


class Listeners(Cog, StatusMessage):
    def __init__(self, bot) -> None:
        super().__init__()
        global settings
        self.bot = bot
        self.on = "🌕"
        self.off = "🌑"
        self.refresh = "🔄"

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global settings
        if payload.member.id == self.bot.user.id or payload.channel_id != settings["status_channel_id"]:
            # print("ignored")
            return

        ch = self.bot.get_channel(payload.channel_id)
        # print(payload)

        if payload.emoji.name == self.refresh:
            await self.make_this_msg(ch)

        if payload.emoji.name in [self.on, self.off]:
            params = {
                "type": "command",
                "idx": settings["switch_id"],
                "param": "switchlight",
                "switchcmd": "Set Level",
                "level": 10 if payload.emoji.name == self.on else 20
            }
            self.send_request(params)
            # Nie trzeba robić żadnego aktualizowania wiadomości,
            # bo zostaną wysłane wiadomosci na kanał "logi". Funckja
            # poniżej to wyłapie i sama zrobi update

    @Cog.listener()
    async def on_message(self, msg):
        if msg.author.id == self.bot.user.id:
            return

        if msg.content.startswith(self.bot.command_prefix):
            # print("It's not for me")
            return
        if msg.channel.id == settings["shell_channel_id"]:
            print("Do wykonania:", msg.content)

        elif msg.channel.id == settings["logs_channel_id"]:
            ''' Aktualizowanie wiadomości "Status" '''
            await self.make_this_msg(msg.guild.get_channel(settings["status_channel_id"]))

def setup(bot):
    bot.add_cog(Listeners(bot))
