import logging
import platform
import time
from typing import Optional
from discord import app_commands

import discord
import psutil
from discord.ext import commands
#from paginator import Paginator, Page, NavigationType
from utils.paginator import Paginator

log = logging.getLogger(__name__)


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.paginator = Paginator(bot)


    '''@commands.command(
        description="Shows the help menu or information for a specific command when specified.",
        usage="help [command]",
        aliases=["h"],
    )'''
    @app_commands.command(name="help",description="Shows the help menu or information for a specific command when specified.")
    async def help(self, ctx, *, command: str = None):
        if command:
            try:
                command = self.bot.tree.get_command(command.lower())
            except:
                command = self.bot.get_command((command.lower()))
            if not command:
                await ctx.response.send_message(
                    embed=discord.Embed(
                        description=f"That command does not exist. Use `/help` to see all the commands.",
                        colour=self.bot.primary_colour,
                    )
                )
                return
            embed = discord.Embed(
                title=command.name,
                description=command.description,
                colour=self.bot.primary_colour,
            )
            await ctx.response.send_message(embed=embed)
            return

        page = discord.Embed(
            title=f"{self.bot.user.name} Commands Menu",
            description="See all commmands brief, use /help to see the more detailed versions.",
            colour=self.bot.primary_colour,
        )
        page.set_thumbnail(url=self.bot.user.avatar)
        page.add_field(
            name="Invite",
            value=f"[Invite Link](https://discord.com/oauth2/authorize?client_id=1061478860832641094&permissions=268823640&scope=bot+applications.commands)",
        )
        page.add_field(name="Support Server", value="https://discord.gg/Y2nDcYzQMn", inline=False)
        page.add_field(name="Donate", value="https://ko-fi.com/ktxdym", inline=False)
        page.set_thumbnail(url=self.bot.user.avatar)
        for _, cog_name in enumerate(self.bot.cogs):
            if cog_name in ["Owner", "Admin"]:
                continue
            cog = self.bot.get_cog(cog_name)
            cog_commands = cog.get_app_commands()
            if len(cog_commands) == 0:
                continue
            cmds = "```\n"
            for cmd in cog_commands:
                cmds += cmd.name + "\n"
            cmds += "```"
            if cog_name == "More":
                cog_name = "Random 2.0"
            page.add_field(name=cog_name, value=cmds)

        await ctx.response.send_message(embed=page)
        

    @commands.command(description="Shows brief help menu", usage="commands", name="commands")
    async def _commands(self, ctx):
        page = discord.Embed(
            title=f"{self.bot.user.name} Commands Menu",
            description="See all commmands brief, use /help to see the more detailed versions.",
            colour=self.bot.primary_colour,
        )
        page.set_thumbnail(url=self.bot.user.avatar)
        page.add_field(
            name="Invite",
            value=f"[Invite Link](https://discord.com/oauth2/authorize?client_id=606402391314530319&permissions=268823640&scope=bot+applications.commands)",
        )
        page.add_field(name="Support Server", value="https://discord.gg/ZatYnsX", inline=False)
        page.add_field(name="Donate", value="https://paypal.me/kym2k06", inline=False)
        page.set_thumbnail(url=self.bot.user.avatar)
        for _, cog_name in enumerate(self.bot.cogs):
            if cog_name in ["Owner", "Admin"]:
                continue
            cog = self.bot.get_cog(cog_name)
            cog_commands = cog.get_commands()
            if len(cog_commands) == 0:
                continue
            cmds = "```\n"
            for cmd in cog_commands:
                if cmd.hidden is False:
                    cmds += cmd.name + "\n"
            cmds += "```"
            if cog_name == "More":
                cog_name = "Random 2.0"
            page.add_field(name=cog_name, value=cmds)

        await ctx.response.send_message(embed=page)

#@commands.command(description="Pong! Get my latency.", usage="ping")
    @app_commands.command(name="ping", description="Pong! Get my latency.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Pong!",
                description=f"Gateway latency: {round(self.bot.latency * 1000, 2)}ms.\n",
                colour=self.bot.primary_colour,
            )
        )
        print(self.bot.tree.get_commands())
    @app_commands.command(name="donate", description="Donate to the bot!")
    async def donate(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Looking to donate? Donate At least 3 USD to get the patron role!!",
            description="As the bot grows, so must our hosting servers. Please support us for us to get better hosting, and motivating us to spend more time developing the bot! Here's [the link](https://ko-fi.com/ktxdym).",
            colour=self.bot.primary_colour,
        )
        

        await interaction.response.send_message(embed=embed)

    def get_bot_uptime(self, *, brief=False):
        hours, remainder = divmod(int(self.bot.uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        if not brief:
            if days:
                fmt = "{d} days, {h} hours, {m} minutes, and {s} seconds"
            else:
                fmt = "{h} hours, {m} minutes, and {s} seconds"
        else:
            fmt = "{h}h {m}m {s}s"
            if days:
                fmt = "{d}d " + fmt
        return fmt.format(d=days, h=hours, m=minutes, s=seconds)


    @app_commands.command(name="stats", description= "See some cool statistics about me.")
    async def stats(self, ctx):
        guilds = len(self.bot.guilds)
        users = len(self.bot.users)
        channels = sum([len(g.channels) for g in self.bot.guilds])
        embed = discord.Embed(title=f"{self.bot.user.name} Statistics", colour=self.bot.primary_colour)
        embed.add_field(
            name="Owners",
            value="kym#6342",
        )
        embed.add_field(name="Bot Version", value=self.bot.version)
        embed.add_field(name="Uptime", value=self.get_bot_uptime(brief=True))
        if ctx.guild:
            embed.add_field(name="Shards", value=f"{ctx.guild.shard_id + 1}/{self.bot.shard_count}")
        else:
            embed.add_field(name="Shards", value=f"{self.bot.shard_count}")
        embed.add_field(name="Servers", value=str(guilds))
        embed.add_field(name="Channels", value=str(channels))
        embed.add_field(name="Users", value=str(users))
        embed.add_field(name="CPU Usage", value=f"{psutil.cpu_percent()}%")
        embed.add_field(name="RAM Usage", value=f"{psutil.virtual_memory().percent}%")
        embed.add_field(name="Python Version", value=platform.python_version())
        embed.add_field(name="discord.py Version", value=discord.__version__)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.add_field(name="Statcord", value="https://statcord.com/bot/606402391314530319")
        embed.set_footer(
            text="</> with ❤ using discord.py",
            icon_url="https://www.python.org/static/opengraph-icon-200x200.png",
        )
        await ctx.response.send_message(embed=embed)

    @app_commands.command(name="invite", description="Get an invite link for the bot.")
    #@commands.command(description="Get a link to invite me.", usage="invite")
    async def invite(self, ctx):
        await ctx.response.send_message(
            embed=discord.Embed(
                title="Invite Link",
                description=f"https://discord.com/oauth2/authorize?client_id=1061478860832641094&permissions=268823640&scope=bot+applications.commands",
                colour=self.bot.primary_colour,
            )
        )


    @app_commands.command(name="support", description="Get a link to my support server.")
    async def support(self, ctx):
        await ctx.response.send_message(
            embed=discord.Embed(
                title="Support Server",
                description="https://discord.gg/Y2nDcYzQMn",
                colour=self.bot.primary_colour,
            )
        )

    @app_commands.command(name="website", description="Get a link to my website.")
    async def website(self, ctx):
        await ctx.response.send_message(
            embed=discord.Embed(
                title="Website",
                description="https://discord.gg/Y2nDcYzQMn",
                colour=self.bot.primary_colour,
            )
        )



async def setup(bot):
    await bot.add_cog(General(bot))
