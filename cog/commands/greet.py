from discord import Role, TextChannel
from discord.app_commands import Choice, choices, describe
from discord.ext import commands
from discord.ext.commands import Context, hybrid_group
from sqlmodel import select

from main import Mapler
from service.db import models

from .. import ABCCog


class Greeting(ABCCog, name="Greeting"):
    def __init__(self, bot: Mapler):
        super().__init__(bot)

    @hybrid_group(
        name="welcome",
        description="Setup your welcome greeting interactively!",
        with_app_command=True,
    )
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx: Context):
        await ctx.defer()

        self.session.add(
            models.Cog(
                name=ctx.cog.qualified_name, description="Commands for greeting feature"
            )
        )

        self.session.add(
            models.Action(
                name="welcome",
                description="Welcome greeting for new members of the server",
            )
        )
        self.session.commit()

        await ctx.reply("Successfully registered welcome action!", ephemeral=True)

    @welcome.command(
        name="message",
        description="Set my welcome message whenever a user joins.",
    )
    @describe(
        message="A text welcome message.",
        embed="An embed welcome message. Must be in an embed JSON format",
    )
    async def welcome_message(
        self,
        ctx: Context,
        message: str | None = None,
        embed: str | None = None,
    ):
        await ctx.defer()

        if message is None and embed is None:
            await ctx.reply("No welcome messages set.")
            return

        cog = self.session.exec(
            select(models.Cog).where(models.Cog.name == ctx.command.cog_name)
        ).one()

        action = self.session.exec(
            select(models.Action).where(
                models.Action.name == ctx.command.root_parent.name
                and models.Action.cog_id == cog.id
            )
        ).one()

        greeting = self.session.exec(
            select(models.ActionGreeting).where(
                models.ActionGreeting.action_id == action.id,
                models.ActionGreeting.guild_id == ctx.guild.id,
            )
        ).one_or_none()

        if greeting:
            greeting.welcome_msg = message or greeting.welcome_msg
            greeting.welcome_embed = embed or greeting.welcome_embed
        else:
            greeting = models.ActionGreeting(
                action_id=action.id,
                guild_id=ctx.guild.id,
                welcome_msg=message,
                welcome_embed=embed,
            )

        self.session.add(greeting)
        self.session.commit()

        await ctx.reply("Successfully configured welcome message!", ephemeral=True)

    @welcome.command(
        name="channel",
        description="Set the channel where welcome messages will be sent.",
    )
    @describe(
        channel="Text channel to send the welcome message to. Defaults to the channel the command is invoked in.",
    )
    async def welcome_channel(self, ctx: Context, channel: TextChannel | None):
        await ctx.defer()

        if not channel:
            channel = ctx.channel

        cog = self.session.exec(
            select(models.Cog).where(models.Cog.name == ctx.command.cog_name)
        ).one()

        action = self.session.exec(
            select(models.Action).where(
                models.Action.name == ctx.command.root_parent.name
                and models.Action.cog_id == cog.id
            )
        ).one()

        greeting = self.session.exec(
            select(models.ActionGreeting).where(
                models.ActionGreeting.action_id == action.id,
                models.ActionGreeting.guild_id == ctx.guild.id,
            )
        ).one_or_none()

        if greeting:
            greeting.welcome_ch = channel.id or greeting.welcome_ch
        else:
            greeting = models.ActionGreeting(
                action_id=self.session.get(models.Action, ident=1).id,
                guild_id=ctx.guild.id,
                welcome_ch=channel.id,
            )

        self.session.add(greeting)
        self.session.commit()

        await ctx.reply(
            "Successfully configured welcome message channel!", ephemeral=True
        )

    @welcome.command(
        name="trigger",
        description="Set the trigger to invoke the welcome greeting.",
    )
    @describe(
        trigger="Trigger event that invokes the greeting. Defaults to when a member joins.",
        role="Role the member must have to trigger the greeting. Defaults to none.",
    )
    @choices(
        triggers=[
            Choice(name="Join", value="on_member_join"),
            Choice(name="Receive Role", value="on_member_update"),
        ]
    )
    async def welcome_trigger(
        self,
        ctx: Context,
        trigger: Choice[str] | None = None,
        role: Role | None = None,
    ):
        await ctx.defer()

        if not trigger:
            trigger = Choice(name="Join", value="on_member_join")

        if trigger.value == "on_member_update" and not role:
            await ctx.reply("No role to attach the trigger to.")
            return

        cog = self.session.exec(
            select(models.Cog).where(models.Cog.name == ctx.command.cog_name)
        ).one()

        action = self.session.exec(
            select(models.Action).where(
                models.Action.name == ctx.command.root_parent.name
                and models.Action.cog_id == cog.id
            )
        ).one()

        greeting = self.session.exec(
            select(models.ActionGreeting).where(
                models.ActionGreeting.action_id == action.id,
                models.ActionGreeting.guild_id == ctx.guild.id,
            )
        ).one_or_none()

        if greeting:
            greeting.welcome_trig = (
                f"{trigger.value}{f'|{role.id}' if role else ''}"
                or greeting.welcome_trig
            )
        else:
            greeting = models.ActionGreeting(
                action_id=action.id,
                guild_id=ctx.guild.id,
                welcome_trig=f"{trigger.value}{f'|{role.id}' if role else ''}",
            )

        self.session.add(greeting)
        self.session.commit()

        await ctx.reply("Successfully configured welcome trigger!", ephemeral=True)


async def setup(bot: Mapler):
    await bot.add_cog(Greeting(bot))
