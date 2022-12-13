import time

import discord
from discord import Option
from discord.ext import commands, tasks
import logging

import embeds
import tools


class TrialSubscription(commands.Cog):
    def __init__(self, bot, config, link_members, plex_account, plex_server, link_trial):
        """
        Cog initialization
        :param bot : Bot object
        :param config: Dict to store config
        """
        self.bot = bot
        self.config = config
        self.link_members = link_members
        self.plex_account = plex_account
        self.plex_server = plex_server
        self.link_trial = link_trial

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Launches when the cog starts
        """
        logging.info(f"Cog Role Trial Subscription Started !")
        self.trial_period_monitoring.start()

    @tasks.loop(seconds=60)
    async def trial_period_monitoring(self):
        """
        Monitoring free trial subscription
        """
        list_delete_id = []
        list_trial = tools.read_trial(self.link_trial)
        for user_id, time_trial in list_trial.items():
            if time.time() > time_trial != 0:
                list_delete_id.append(user_id)
        if list_delete_id:
            guild = self.bot.get_guild(self.config['guild_id'])
            for role in guild.roles:
                if str(role) == f"{self.bot.user.name} - {self.config['role_subscriber']}":
                    role_subscriber = role
                    break
            for user_id in list_delete_id:
                user = guild.get_member(int(user_id))
                await user.remove_roles(role_subscriber)
                tools.write_trial(self.link_trial, user_id, 0)
                await user.send(embed=await embeds.end_trial(self.config))

    @discord.slash_command(description="Request a free trial subscription for a limited time")
    async def trial_subscription(self,
                                 ctx):
        """
        Free trial subscription for a limited time
        :param ctx: Message context
        """
        logging.info(f"DISCORD: Request a trial subscription by {ctx.author.name}")
        already_trial = tools.read_trial(self.link_trial)
        if str(ctx.author.id) in already_trial:
            await ctx.respond(embed=await embeds.already_tested(self.config),
                              ephemeral=True)
            return
        response = await ctx.respond(
            embed=await embeds.in_progress(self.config), ephemeral=True)
        list_roles = []
        guild = self.bot.get_guild(self.config['guild_id'])
        for role in guild.roles:
            if str(role)[:len(self.bot.user.name) + 3] == f"{self.bot.user.name} - " and str(
                    role) != f"{self.bot.user.name} - {self.config['role_subscriber']}":
                list_roles.append(role)
            if str(role) == f"{self.bot.user.name} - {self.config['role_subscriber']}":
                role_subscriber = role
        await ctx.author.add_roles(*list_roles)
        await ctx.author.add_roles(role_subscriber)
        tools.write_trial(self.link_trial, ctx.author.id, time.time() + 3600 * self.config['test_duration'])
        await response.edit_original_message(
            embed=await embeds.launch_trial(self.config))
        if self.config['private_channel_id'] != 0:
            private_channel = self.bot.get_channel(self.config['private_channel_id'])
            await private_channel.send(embed=await embeds.private_new_trial(self.config, ctx.author))

    @discord.slash_command(description="Reset free trial subscription for a user")
    async def reset_trial_subscription(self,
                                       ctx,
                                       user: Option(discord.User, "Select the user to delete")):
        """
        Reset free trial subscription for a user
        :param ctx: Message context
        :param user: User object
        """
        if ctx.author.guild_permissions.administrator:
            logging.info(f"DISCORD: Reset a trial subscription for {user} by {ctx.author.name}")
            success = tools.delete_trial(self.link_trial, str(user.id))
            if success:
                await ctx.respond(
                    embed=await embeds.reset_trial(self.config),
                    ephemeral=True)
                return
            await ctx.respond(
                embed=await embeds.never_tested(self.config),
                ephemeral=True)
        else:
            await ctx.respond(embed=await embeds.unauthorized(self.config),
                              ephemeral=True)

    @discord.slash_command(description="Offer a subscription to a user for limited time")
    async def gift_subscription(self,
                                ctx,
                                user: Option(discord.User, "Select the user to whom to offer the subscription"),
                                time_limit: Option(int, "Validity time in hours")):
        """
        Offer a subscription to a user for limited time
        :param ctx: Message context
        :param user: User object
        :param time_limit: Validity time in hours
        """
        if ctx.author.guild_permissions.administrator:
            logging.info(f"DISCORD: Offer a subscription for {user} by {ctx.author.name} ({time_limit} hours)")
            response = await ctx.respond(
                embed=await embeds.in_progress(self.config), ephemeral=True)
            list_roles = []
            guild = self.bot.get_guild(self.config['guild_id'])
            for role in guild.roles:
                if str(role)[:len(self.bot.user.name) + 3] == f"{self.bot.user.name} - " and str(
                        role) != f"{self.bot.user.name} - {self.config['role_subscriber']}":
                    list_roles.append(role)
                if str(role) == f"{self.bot.user.name} - {self.config['role_subscriber']}":
                    role_subscriber = role
            await user.add_roles(*list_roles)
            await user.add_roles(role_subscriber)
            tools.write_trial(self.link_trial, user.id, time.time() + 3600 * time_limit)
            await response.edit_original_message(
                embed=await embeds.launch_trial(self.config))
        else:
            await ctx.respond(embed=await embeds.unauthorized(self.config),
                              ephemeral=True)
