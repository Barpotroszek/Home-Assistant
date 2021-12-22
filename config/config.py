import json
from os import makedirs, walk
from os.path import join
from discord import Color, Embed
from discord.channel import TextChannel
from discord.errors import HTTPException
from requests import get

DATA_DIR_PATH = "path"
COGS_DIR_PATH = "cogs"
SECRETS_PATH = "secrets"
CONFIG_FILE_PATH = f"{SECRETS_PATH}/config.json"
TOKEN = open(f"{SECRETS_PATH}/token", "r").read()
GUILD_ID = open(f"{SECRETS_PATH}/guild_id", "r").read()
__cogs__ = []


class _json:
    def __init__(self, path) -> None:
        self.path = path

    def read(self) -> dict:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def write(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def __cogs__():
    __cogs__ = []
    for (path, dirs, files) in walk(COGS_DIR_PATH):
        for file in files:
            # print(file)
            if file.endswith(".py"):
                path_to_file = join(path, file[:-3])
                table = path_to_file.maketrans("\\", ".")  # for Windows
                path_to_file = path_to_file.translate(table)
                table = path_to_file.maketrans("/", ".")  # for Linux
                __cogs__.append(path_to_file.translate(table))
    return __cogs__


async def startup(bot):
    global settings
    from os.path import isfile
    if not isfile(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "a") as f:
            f.write("{}")
            f.close()
    
    settings = _json(CONFIG_FILE_PATH).read()
    if all(b for _, b in settings.items()) and len(settings) == 7:
        return

    async def get_channel_by_name(name: str) -> TextChannel:
        guild = bot.get_guild(GUILD_ID)
        for ch in bot.get_all_channels():
            if ch.name == name:
                return ch.id
        ch = await guild.create_text_channel(name)
        return ch.id

    settings = {
        "logs_channel_id": await get_channel_by_name("logi"),
        "status_channel_id": await get_channel_by_name("status"),
        "commands_channel_id": await get_channel_by_name("commands"),
        "shell_channel_id": await get_channel_by_name("shell"),
        "status_msg_id": None,
        "switch_id": 4,
        "device_id": 14
    }
    _json(CONFIG_FILE_PATH).write(settings)


class StatusMessage:
    '''Klasa zarządzająca wiadomościami statusu urządzeń'''
    def send_request(self, params):
        return get(
            url="http://192.168.0.147:8080/json.htm",
            params=params
        )

    async def update_status_msg(self, msg):
        '''
        Aktualizowanie wiadomości przedstawiającej status urządzenia,
        którego ID jest zdefiniowane w pliku konfiguracyjnym
        '''
        info_params = {
            "type": "devices",
            "rid": settings["device_id"]
        }

        response = self.send_request(info_params)
        # print(response.text)
        emb = Embed()
        if response.status_code != 200:
            emb.title = "Request"
            emb.add_field(name="URL:", value=response.url)
            emb.add_field(name="Status code:", value=response.status_code)

        else:
            data_json = json.loads(response.text)
            data = data_json["result"][0]
            status = data["Status"]
            emb.title = "``` Device Info ```"
            emb.add_field(name="ID:", value=data["idx"])
            emb.add_field(name="Name:", value=data["Name"], inline=True)
            emb.add_field(name="Last device update:",
                          value=data["LastUpdate"], inline=True)
            emb.add_field(name="Status:", value=status, inline=True)
            emb.color = Color.from_rgb(
                227, 210, 98) if status == "On" else Color.default()

        emb.set_footer(
            text=F"Message updated at: {data_json['ServerTime']}")

        # print(response.text)
        await msg.clear_reactions()
        await msg.edit(embed=emb)
        await msg.add_reaction(self.on if status == "Off" else self.off)
        await msg.add_reaction(self.refresh)

    async def make_this_msg(self, channel):
        '''Wysyłanie wiadomości "na czekanie" i tej właściwej xd'''
        emb = Embed(
            title="```Work in progress```",
            description="Please wait"
        )
        try:
            msg = await channel.fetch_message(settings["status_msg_id"])
            await msg.clear_reactions()
            await msg.edit(embed=emb)
        except HTTPException:
            msg = await channel.send(embed=emb)
            settings["status_msg_id"] = msg.id
            _json(CONFIG_FILE_PATH).write(settings)
        await self.update_status_msg(msg)
