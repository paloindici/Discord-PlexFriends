import sys
import discord
import plexapi.server
from discord.ext import commands
import logging

import cog_admin_commands
import cog_donatebot
import cog_role_monitoring
import cog_trial_subscription
import generate_files
import plex
import tools

bot_version = "0.0.13"

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s:%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logging.getLogger('discord.client').disabled = True
logging.getLogger('discord.gateway').disabled = True
logging.getLogger('plexapi').disabled = True

# On first run, generate config file and exit
link_config = generate_files.locate('/config/config.json')
if link_config is None:
    logging.error("INIT: No config file found, generating empty config file...")
    generate_success = generate_files.generate_empty_config()
    if generate_success:
        logging.info("INIT: Empty config generated in /config path. Please fill config.json before restarting bot.")
    else:
        logging.info("INIT: Unable to generate config file. Check your /config volume.")
    sys.exit()
else:
    # Load Config file
    logging.info("INIT: Config file found")
    config = tools.read_config(f"{link_config}config.json")
    # Check if config file is populated before continuing
    if config['bot_token'] == "" or config['guild_id'] == 0 or config['role_subscriber'] == "" or config['plex_user'] == "" or config['plex_password'] == "" or config['plex_url'] == "" or config['plex_token'] == "":
        logging.error("INIT: Config file not populated. Please fill config.json before restarting bot.")
        sys.exit()
    config['version'] = bot_version

# locate or create members file
link_members = generate_files.locate_generate_empty_members(link_config)
if link_members is None:
    logging.error("INIT: Member file not found. Exit the bot.")
    sys.exit()

if 'test_duration' in config:
    if config['test_duration'] != 0:
        # locate or create trial file
        link_trial = generate_files.locate_generate_trial_subscription(link_config)
        if link_trial is None:
            logging.error("INIT: Trial file not found. Exit the bot.")
            sys.exit()

if 'donate_api' in config:
    if config['donate_api'] != "":
        # locate or create history file
        link_history_transactions = generate_files.locate_generate_history_transactions(link_config)
        if link_history_transactions is None:
            logging.error("INIT: History Transactions file not found. Exit the bot.")
            sys.exit()
        # locate or create subscription file
        link_subscription = generate_files.locate_generate_subscription(link_config)
        if link_subscription is None:
            logging.error("INIT: Subscription file not found. Exit the bot.")
            sys.exit()

config['messages'] = tools.init_language(link_config)

# Initialize connection with Plex
plex_account = plex.plex_login(config['plex_user'], config['plex_password'])
plex_server = plexapi.server.PlexServer(config['plex_url'], config['plex_token'])

# Initialize discord.py client
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)
bot.remove_command('help')

# Cog RoleMonitoring
bot.add_cog(cog_role_monitoring.RoleMonitoring(bot, config, link_members, plex_account, plex_server))

# Cog AdminCommands
bot.add_cog(cog_admin_commands.AdminCommands(bot, config, link_members, plex_account, plex_server))

if 'test_duration' in config:
    if config['test_duration'] != 0:
        bot.add_cog(cog_trial_subscription.TrialSubscription(bot, config, link_members, plex_account, plex_server,
                                                             link_trial))

if 'donate_api' in config:
    if config['donate_api'] != "":
        bot.add_cog(cog_donatebot.DonateBot(bot, config, link_members, plex_account, plex_server,
                                            link_history_transactions, link_subscription))

# Run bot
bot.run(config['bot_token'])
