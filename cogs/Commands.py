import typing
from config.config import settings, CONFIG_FILE_PATH, _json, StatusMessage
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(
        name="set_idx", usage="<device|switch> <idx>", aliases=["idx"],
        help="Ustawia ID urządzenia, o którym ma szukać informacji, lub przełącznika",
    )
    async def set_new_id(self, ctx, device_name=None, id: int = None):
        if not device_name:
            return await ctx.send("```Musisz podać urządzenie: device lub switch```")
        if not id:
            return await ctx.send(f"{device_name}_id: **{settings[f'{device_name}_id']}**")
        settings[f"{device_name}_id"] = id
        _json(CONFIG_FILE_PATH).write(settings)
        await ctx.send(f"Ustawiono *{device_name}_id* jako: {settings[f'{device_name}_id']}")

    @commands.command(name="switch", usage="<on|off|0|1>", help="Włącza/Wyłącza urządzenie")
    async def switch_device(self, ctx, state: typing.Union[int, str]):
        params = {
                "type": "command",
                "idx": settings["switch_id"],
                "param": "switchlight",
                "switchcmd": "Set Level",
            }
        if state in [1, "on"]:
            await ctx.send("Device będzie włączone")
            params['level'] = 10

        elif state in [0, "off"]:
            await ctx.send("Device będzie wyłączone")
            params['level'] = 10

        else:
            await ctx.send("*Podano złe argumenty :D*")
            return
        StatusMessage().send_request(params)

def setup(bot):
    bot.add_cog(Commands(bot))
