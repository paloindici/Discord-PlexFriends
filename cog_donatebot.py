import time

import discord
from discord.ext import commands, tasks
import logging

import donate
import embeds
import tools


class DonateBot(commands.Cog):
    def __init__(self, bot, config, link_members, plex_account, plex_server, link_history_transactions,
                 link_subscription):
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
        self.link_history_transactions = link_history_transactions
        self.link_subscription = link_subscription

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Launches when the cog starts
        """
        logging.info(f"Cog DonateBot Started !")
        self.monitoring_new_donations.start()
        self.monitoring_end_of_subscription.start()

    @tasks.loop(seconds=60)
    async def monitoring_new_donations(self):
        """
        Monitoring new donations
        """
        new_donates = donate.new_donation(self.config['donate_api'], self.config['guild_id'], find='Completed')
        if new_donates is not None:
            new_donates = new_donates['donations']
            old_donates = tools.read_history_transactions(self.link_history_transactions)
            news_difference = [x for x in new_donates if x not in old_donates]
            if news_difference:
                list_roles = []
                guild = self.bot.get_guild(self.config['guild_id'])
                for role in guild.roles:
                    if str(role)[:len(self.bot.user.name) + 3] == f"{self.bot.user.name} - " and str(
                            role) != f"{self.bot.user.name} - {self.config['role_subscriber']}":
                        list_roles.append(role)
                    if str(role) == f"{self.bot.user.name} - {self.config['role_subscriber']}":
                        role_subscriber = role
                for new_donate in news_difference:
                    user = guild.get_member(int(new_donate['buyer_id']))
                    valid = False
                    for roles_lib in list_roles:
                        if roles_lib in user.roles:
                            valid = True
                            break
                    if not valid:
                        await user.add_roles(*list_roles)
                    await user.add_roles(role_subscriber)
                    tools.write_subscription(self.link_subscription, new_donate['buyer_id'])
                    tools.write_history_transactions(self.link_history_transactions, new_donate)
                    if self.config['private_channel_id'] != 0:
                        private_channel = self.bot.get_channel(self.config['private_channel_id'])
                        await private_channel.send(embed=await embeds.private_new_subscription(self.config, user))
            else:
                print("No new donation")

    @tasks.loop(seconds=600)
    async def monitoring_end_of_subscription(self):
        """
        Monitoring end of subscription
        """
        subscription = tools.read_subscription(self.link_subscription)
        end_subscription = []
        pre_end_subscription = []
        for user, end_time in subscription.items():
            if end_time != 0 and end_time < int(time.time()):
                end_subscription.append(user)
            if end_time != 0 and int(time.time()) - 300 < end_time - 172800 < int(time.time()) + 300:
                pre_end_subscription.append(user)
        if end_subscription:
            guild = self.bot.get_guild(self.config['guild_id'])
            for role in guild.roles:
                if str(role) == f"{self.bot.user.name} - {self.config['role_subscriber']}":
                    role_subscriber = role
            for user in end_subscription:
                user_discord = guild.get_member(int(user))
                await user_discord.remove_roles(role_subscriber)
                tools.write_end_subscription(self.link_subscription, user)
                await user_discord.send(embed=await embeds.end_subscription(self.config))
                if self.config['private_channel_id'] != 0:
                    private_channel = self.bot.get_channel(self.config['private_channel_id'])
                    await private_channel.send(embed=await embeds.private_end_subscription(self.config, user))
        if pre_end_subscription:
            guild = self.bot.get_guild(self.config['guild_id'])
            for user in pre_end_subscription:
                user = guild.get_member(int(user))
                await user.send(embed=await embeds.pre_end_subscription(self.config))

    @discord.slash_command(description="Order a subscription")
    async def subscription(self,
                           ctx):
        """
        Order a subscription
        :param ctx: Message context
        """
        logging.info(f"DONATE: Subscription request by {ctx.user}")
        guild = self.bot.get_guild(self.config['guild_id'])
        list_roles = []
        options = []
        for role in guild.roles:
            if str(role)[:len(self.bot.user.name) + 3] == f"{self.bot.user.name} - " and str(
                    role) != f"{self.bot.user.name} - {self.config['role_subscriber']}":
                list_roles.append(role)
        for role in list_roles:
            lib_name = str(role)[len(self.bot.user.name) + 3:]
            options.append(discord.SelectOption(label=lib_name))

        await ctx.respond(embed=await embeds.subscription_in_progress(self.config), ephemeral=True)
        await ctx.user.send(embed=await embeds.subscription1(self.config),
                            view=SelectView(options, self.config, guild, self.bot))

    @discord.slash_command(description="Overview of current subscriptions")
    async def current_subscriptions(self,
                                    ctx):
        """
        Overview of current subscriptions
        :param ctx: Message context
        """
        if ctx.author.guild_permissions.administrator:
            subscription = tools.read_subscription(self.link_subscription)
            current = {}
            message = ""
            if subscription:
                guild = self.bot.get_guild(self.config['guild_id'])
                for user in subscription.keys():
                    if subscription[user] != 0:
                        username = guild.get_member(int(user))
                        current[user] = subscription[user]
                        message += f'{username} - <t:{subscription[user]}>\n'
                await ctx.respond(embed=await embeds.current_subscriptions(message, self.config), ephemeral=True)
            else:
                await ctx.respond(embed=await embeds.unauthorized(self.config),
                                  ephemeral=True)


class Select(discord.ui.Select):
    def __init__(self, options, config, guild, bot):
        super().__init__(placeholder="Library", max_values=len(options), min_values=1, options=options)
        self.config = config
        self.guild = guild
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        await interaction.message.edit(view=None, embed=await embeds.subscription2(self.config))
        list_roles = []
        lib_roles = []
        for role in self.guild.roles:
            if str(role)[:len(self.bot.user.name) + 3] == f"{self.bot.user.name} - " and str(
                    role) != f"{self.bot.user.name} - {self.config['role_subscriber']}":
                list_roles.append(role)
        for role in list_roles:
            for selected in self.values:
                if str(role)[len(self.bot.user.name) + 3:] == selected:
                    lib_roles.append(role)
        user = self.guild.get_member(int(interaction.user.id))
        await user.add_roles(*lib_roles)


class SelectView(discord.ui.View):
    def __init__(self, options, config, guild, bot, *, timeout=180):
        super().__init__(timeout=timeout)
        self.config = config
        self.add_item(Select(options, config, guild, bot))

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(embed=await embeds.select_lib_timeout(self.config), view=self)
