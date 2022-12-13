import re

from discord.ext import commands
import logging

import embeds
import overseerr
import plex
import tools


class RoleMonitoring(commands.Cog):
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
        self.role_subscriber = ""
        self.list_roles_library = []
        self.lock_role = False
        self.email_waiting = []

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Launches when the cog starts
        """
        logging.info(f"Cog Role Monitoring Started !")
        guild = self.bot.get_guild(self.config['guild_id'])
        sections = self.plex_server.library.sections()
        for section in sections:
            self.list_roles_library.append(f"{self.bot.user.name} - {section.title}")
            exist = False
            role_name = self.bot.user.name + " - " + section.title
            for role in guild.roles:
                if str(role) == role_name:
                    exist = True
            if not exist:
                await guild.create_role(name=role_name)
        role_subscriber_exist = False
        self.role_subscriber = self.bot.user.name + " - " + self.config['role_subscriber']
        for role in guild.roles:
            if str(role) == self.role_subscriber:
                role_subscriber_exist = True
        if not role_subscriber_exist:
            await guild.create_role(name=self.role_subscriber)

    # Watch the roles
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if self.lock_role:
            self.lock_role = False
        else:
            if len(before.roles) < len(after.roles):
                # Add role
                role = list(set(after.roles) - set(before.roles))[0]
                print(role)
                if str(role) == self.role_subscriber:
                    # Role subscriber
                    await self.add_role_subscriber(after, role)
                if str(role) in self.list_roles_library:
                    # Role library
                    await self.add_role_library(after, role)

            elif len(before.roles) > len(after.roles):
                # Delete role
                role = list(set(before.roles) - set(after.roles))[0]
                if str(role) == self.role_subscriber:
                    # Role subscriber
                    await self.del_role_subscriber(after, role)
                if str(role) in self.list_roles_library:
                    # Role library
                    await self.del_role_library(after, role)

    async def add_role_subscriber(self, member, role):
        valid = False
        for role_member in member.roles:
            if str(role_member) in self.list_roles_library:
                valid = True
                break
        if valid:
            members = tools.read_member(self.link_members)
            if str(member.id) not in members and member.id not in self.email_waiting:
                # Not in database and not wait email
                self.email_waiting.append(member.id)
                user_email = await self.get_user_email(self.bot, member)
                if user_email is None:
                    # Email not valid
                    self.email_waiting.remove(member.id)
                    return
                self.email_waiting.remove(member.id)
                tools.add_member(self.link_members, member.id, user_email)
            elif str(member.id) in members and member.id not in self.email_waiting:
                # In the database and not wait email
                if plex.is_friends(members[str(member.id)], self.plex_account):
                    # Is already in Plex Friends
                    return
                if plex.is_pending(members[str(member.id)], self.plex_account):
                    # Is pending accept friend
                    return
                user_email = members[str(member.id)]
            else:
                return
            sections = plex.select_library(self.bot.user.name, self.plex_server, member.roles)
            plex.add_user(self.plex_account, user_email, self.plex_server, sections)
            if self.config['overseerr_url'] != "":
                overseerr.create_user(self.config['overseerr_api_key'], self.config['overseerr_url'],
                                      user_email)
            await member.send(embed=await embeds.welcome_message(self.config))
        else:
            self.lock_role = True
            await member.remove_roles(role)
            logging.info(
                f"PLEXAPI: Cannot subscribe to {member.display_name} if he has no access to any library")
            return

    async def del_role_subscriber(self, member, role):
        members = tools.read_member(self.link_members)
        if str(member.id) in members:
            # If in the database
            if plex.is_friends(members[str(member.id)], self.plex_account):
                plex.remove_user(self.plex_account, members[str(member.id)])
                await member.send(await embeds.delete_account(self.config))
            elif plex.is_pending(members[str(member.id)], self.plex_account):
                plex.remove_user_pending(self.plex_account, members[str(member.id)])
                await member.send(await embeds.delete_account(self.config))
            if self.config['overseerr_url'] != "":
                overseerr.delete_user(self.config['overseerr_api_key'],
                                      self.config['overseerr_url'],
                                      members[str(member.id)])

    async def add_role_library(self, member, role):
        members = tools.read_member(self.link_members)
        if str(member.id) in members:
            # If in the database
            if plex.is_pending(members[str(member.id)], self.plex_account):
                # If pending accept friend, remove role
                if not self.lock_role:
                    self.lock_role = True
                    await member.remove_roles(role)
                    logging.info(
                        f"PLEXAPI: Unable to update user {members[str(member.id)]}: Plex friend request was not accepted")
                    return
            guild = self.bot.get_guild(self.config['guild_id'])
            for guild_role in guild.roles:
                if str(guild_role) == self.role_subscriber:
                    if guild_role in member.roles:
                        # If member have subscriver role, update libraries
                        sections = plex.select_library(self.bot.user.name, self.plex_server, member.roles)
                        result_update = plex.update_friend(self.plex_account, members[str(member.id)], self.plex_server,
                                                           sections)
                        if not result_update and member.id not in self.email_waiting:
                            self.lock_role = True
                            await member.remove_roles(guild_role)
                            logging.info(
                                f"PLEXAPI: User {members[str(member.id)]} is no longer on the friends list. "
                                f"Deletion of the subscriber role")
                            return
                        logging.info(f"PLEXAPI: Library updated for {members[str(member.id)]}")
                        return

    async def del_role_library(self, member, role):
        members = tools.read_member(self.link_members)
        if str(member.id) in members:
            # If in the database
            if plex.is_pending(members[str(member.id)], self.plex_account):
                # If pending accept friend, add role
                if not self.lock_role:
                    self.lock_role = True
                    await member.add_roles(role)
                    logging.info(
                        f"PLEXAPI: Unable to update user {members[str(member.id)]}: Plex friend request was not accepted")
                    return
            guild = self.bot.get_guild(self.config['guild_id'])
            for guild_role in guild.roles:
                if str(guild_role) == self.role_subscriber:
                    if guild_role in member.roles:
                        # If member have subscriver role, update libraries
                        sections = plex.select_library(self.bot.user.name, self.plex_server, member.roles)
                        result_update = plex.update_friend(self.plex_account, members[str(member.id)], self.plex_server,
                                                           sections)
                        if not result_update and member.id not in self.email_waiting:
                            self.lock_role = True
                            await member.remove_roles(guild_role)
                            logging.info(
                                f"PLEXAPI: User {members[str(member.id)]} is no longer on the friends list. "
                                f"Deletion of the subscriber role")
                            return
                        delete = True
                        for role_member in member.roles:
                            if str(role_member) in self.list_roles_library:
                                delete = False
                                break
                        if delete:
                            await member.remove_roles(guild_role)
                            logging.info(
                                f"PLEXAPI: No more shared libraries for user {members[str(member.id)]}. "
                                f"Deletion of the subscriber role")
                            return
                        logging.info(f"PLEXAPI: Library updated for {members[str(member.id)]}")
                        return

    async def get_user_email(self, bot, user):
        user_email = None
        await user.send(embed=await embeds.ask_for_email(self.config))
        while user_email is None:
            def check_sender(m):
                return m.author == user

            try:
                message = await bot.wait_for('message', timeout=3600, check=check_sender)
                if message.content.lower() == "cancel":
                    await user.send(embed=await embeds.dm_cancelled(self.config))
                    return None
                elif self.check_email(message.content):
                    members = tools.read_member(self.link_members)
                    if message.content in members.values():
                        await user.send(embed=await embeds.email_in_use(self.config))
                    else:
                        user_email = message.content
                        await user.send(embed=await embeds.email_success(self.config))
                else:
                    await user.send(embed=await embeds.invalid_email(self.config))
            except TimeoutError:
                await user.send(embed=await embeds.email_timeout(self.config))
        return user_email

    # Regex method to validate emails
    def check_email(self, address):
        email_filter = "(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"
        return re.match(email_filter, address.lower())
