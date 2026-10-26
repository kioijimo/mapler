import os

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv


class Mapler(Bot):
    def __init__(self):
        super().__init__(command_prefix="m:", intents=discord.Intents.all())
        self.new_members: list[discord.Member] = []

    async def on_ready(self):
        print("Connected to Discord. Logged in as ", self.user)

    async def on_member_join(self, member: discord.Member):
        self.new_members.append(member)

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        MEMBER_ROLE_ID = 1563850519087161344
        MAIN_CHANNEL_ID = 1563706475833204827

        matched = False

        for member in self.new_members:
            if before.id == member.id:
                matched = True
                break

        if not matched:
            return

        found = False

        for role in after.roles:
            if role.id == MEMBER_ROLE_ID:
                found = True
                break

        if not found:
            return

        channel = self.get_channel(MAIN_CHANNEL_ID)

        if isinstance(channel, discord.TextChannel):
            await channel.send(f"Wow new member! Welcome nyo nga si {after.mention}!!")

        self.new_members.remove(before)

    async def on_member_remove(self, member: discord.Member):
        channel = self.get_channel(1563706475833204827)

        if isinstance(channel, discord.TextChannel):
            await channel.send(f"Wow umalis. Kapal ng mukha {member.mention}!!")


if __name__ == "__main__":
    load_dotenv()

    mapler = Mapler()
    mapler.run(str(os.environ.get("TOKEN")))
