import discord
from discord import Option, option
from discord.ext import commands
import logging

import embeds
import overseerr
import plex
import tools


class AdminCommands(commands.Cog):
    def __init__(self, bot, config, link_members, plex_account, plex_server):
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
        self.message_subject = []
        self.in_db = {
            True: '✅',
            False: '❌'
        }

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Launches when the cog starts
        """
        logging.info(f"Cog Admin Commands Started !")
        act = discord.Game(f"v{self.config['version']}")
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(type=discord.ActivityType.competing,
                                                                 name=str(act)))
        for subject in self.config['messages']:
            self.message_subject.append(subject)

    async def get_subjects(self, ctx: discord.AutocompleteContext):
        """Returns a list of collections that begin with the characters entered so far."""
        return [subject for subject in self.message_subject if subject.startswith(ctx.value.lower())]

    @discord.slash_command(description="Delete user from Plex server and database")
    async def delete_user(self,
                          ctx,
                          user: Option(discord.User, "Select the user to delete")):
        """
        Delete user from Plex server and database
        :param ctx: Message context
        :param user: User object
        """
        if ctx.author.guild_permissions.administrator:
            logging.info(f"DISCORD: Force delete user {user}")
            members = tools.read_member(self.link_members)
            if str(user.id) in members:
                user_email = members[str(user.id)]
                plex_exist_users = self.plex_account.users()
                user_deleted = False
                for plex_exist_user in plex_exist_users:
                    if str(plex_exist_user.email) == user_email:
                        plex.remove_user(self.plex_account, user_email)
                        if self.config['overseerr_url'] != "":
                            overseerr.delete_user(self.config['overseerr_api_key'], self.config['overseerr_url'],
                                                  user_email)
                        user_deleted = True
                        break
                if not user_deleted:
                    plex_pending_users = self.plex_account.pendingInvites(includeSent=True, includeReceived=False)
                    for plex_pending_user in plex_pending_users:
                        if str(plex_pending_user.email) == user_email:
                            self.plex_account.cancelInvite(user_email)
                            if self.config['overseerr_url'] != "":
                                overseerr.delete_user(self.config['overseerr_api_key'], self.config['overseerr_url'],
                                                      user_email)
                            break
                guild = self.bot.get_guild(self.config['guild_id'])
                for role in guild.roles:
                    if str(role) == f"{self.bot.user.name} - {self.config['role_subscriber']}":
                        await user.remove_roles(role)
                        break
                tools.delete_member(self.link_members, str(user.id))
                await ctx.respond(
                    embed=await embeds.delete_account_admin(self.config),
                    ephemeral=True)
            else:
                await ctx.respond(embed=await embeds.not_in_db(self.config),
                                  ephemeral=True)
        else:
            await ctx.respond(embed=await embeds.unauthorized(self.config),
                              ephemeral=True)

    @discord.slash_command(description="Delete user from Plex server and database by email address")
    async def delete_user_by_email(self,
                                   ctx,
                                   user_email: Option(str, "User email address")):
        """
        Delete user from Plex server and database
        :param ctx: Message context
        :param user_email: email address
        """
        if ctx.author.guild_permissions.administrator:
            logging.info(f"DISCORD: Force delete user {user_email} from database")
            members = tools.read_member(self.link_members)
            found = False
            for key, value in members.items():
                if value == user_email:
                    found = True
                    tools.delete_member(self.link_members, int(key))
                    plex_exist_users = self.plex_account.users()
                    user_deleted = False
                    for plex_exist_user in plex_exist_users:
                        if str(plex_exist_user.email) == user_email:
                            plex.remove_user(self.plex_account, user_email)
                            if self.config['overseerr_url'] != "":
                                overseerr.delete_user(self.config['overseerr_api_key'], self.config['overseerr_url'],
                                                      user_email)
                            user_deleted = True
                            break
                    if not user_deleted:
                        plex_pending_users = self.plex_account.pendingInvites(includeSent=True, includeReceived=False)
                        for plex_pending_user in plex_pending_users:
                            if str(plex_pending_user.email) == user_email:
                                self.plex_account.cancelInvite(user_email)
                                if self.config['overseerr_url'] != "":
                                    overseerr.delete_user(self.config['overseerr_api_key'],
                                                          self.config['overseerr_url'],
                                                          user_email)
                                break
                    break
            if found:
                await ctx.respond(
                    embed=await embeds.delete_account_admin(self.config),
                    ephemeral=True)
            else:
                await ctx.respond(embed=await embeds.not_in_db(self.config),
                                  ephemeral=True)
        else:
            await ctx.respond(embed=await embeds.unauthorized(self.config),
                              ephemeral=True)

    @discord.slash_command(description="View database content")
    async def get_db(self, ctx):
        """
        View database content
        :param ctx: Message context
        """
        if ctx.author.guild_permissions.administrator:
            members = tools.read_member(self.link_members)
            message = ""
            for key, value in members.items():
                user = self.bot.get_user(int(key))
                message += f"{user.display_name}#{user.discriminator} - {key} - {value}\n"
            embed = await embeds.database_content(message, self.config)
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            await ctx.respond(embed=await embeds.unauthorized(self.config),
                              ephemeral=True)

    @discord.slash_command(description="See the list of all friends on Plex")
    async def view_all_plex_friends(self, ctx):
        """
        See the list of all friends on Plex
        :param ctx: Message context
        """
        if ctx.author.guild_permissions.administrator:
            members = tools.read_member(self.link_members)
            friends = plex.all_users(self.plex_account)
            message = "Member name - Member email - In the database\n\n"
            for friend in friends:
                in_db = False
                for key, value in members.items():
                    if value == friend.email:
                        in_db = True
                        break
                message += f"{friend.title} **-** {friend.email} **-** {self.in_db[in_db]}\n"
            embed = await embeds.database_content(message, self.config)
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            await ctx.respond(embed=await embeds.unauthorized(self.config),
                              ephemeral=True)

    @discord.slash_command(description="Send a welcome message to a member")
    async def send_welcome_message(self,
                                   ctx,
                                   user: Option(discord.User, "Select the user to send welcome message")):
        """
        Send a welcome message to a member
        :param ctx: Message context
        :param user: User object
        """
        if ctx.author.guild_permissions.administrator:
            logging.info(f"DISCORD: Force send welcome message to {user}")
            await user.send(embed=await embeds.welcome_message(self.config))
            await ctx.respond(
                embed=await embeds.confirm_send_welcome(self.config),
                ephemeral=True)
        else:
            await ctx.respond(embed=await embeds.unauthorized(self.config),
                              ephemeral=True)

    @discord.slash_command(description="Preview any message")
    @option("subject", description="Name of the subject", autocomplete=get_subjects)
    async def preview_message(self,
                              ctx,
                              subject: str):
        """
        Preview a message
        :param ctx: Message context
        :param subject: Message subject name
        """
        if ctx.author.guild_permissions.administrator:
            await ctx.respond(embed=await embeds.test_message(self.config,
                                                              self.config['messages'][subject]['title'],
                                                              self.config['messages'][subject]['message']),
                              ephemeral=True)
        else:
            await ctx.respond(embed=await embeds.unauthorized(self.config),
                              ephemeral=True)
