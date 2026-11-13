import logging
import os
from glob import glob

from discord import Activity, ActivityType, Colour, Intents
from discord.ext.commands import Bot
from sqlmodel import Session


class Mapler(Bot):
    def __init__(self, session: Session):
        super().__init__(command_prefix="m:", intents=Intents.all())
        self.session = session
        self.embed_color = Colour.from_str("#f7666a")

    async def load_cogs(self):
        for cog in glob(os.path.join("cog", "*", "*")):
            if os.path.isfile(cog) and cog.endswith(".py"):
                cog_name = cog.split(os.path.sep)[-1][:-3]
                await self.load_extension(
                    f"{'.'.join(cog.split(os.path.sep)[:-1])}.{cog_name}"
                )

    @property
    def logger(self):
        return logging.getLogger()

    def setup_log(self):
        logging.basicConfig(filename="mapler.log", level=logging.INFO)

    async def on_connect(self):
        self.setup_log()

        # self.session.add(models.Guild(id=1563694659484520468, name="sunnyside maple"))

        await self.load_cogs()

    async def on_ready(self):
        await self.change_presence(
            activity=Activity(
                type=ActivityType.watching,
                name=f"Overseeing {len([m for m in self.guilds[0].members if not m.bot])} maplers~",
            )
        )
        print("Connected to Discord. Logged in as", self.user)
