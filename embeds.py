import discord


async def ask_for_email(config):
    embed = discord.Embed(
        color=discord.Color.blue(),
        title=config['messages']['ask_for_email']['title'],
        description=config['messages']['ask_for_email']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def email_success(config):
    embed = discord.Embed(
        color=discord.Color.green(),
        title=config['messages']['email_success']['title'],
        description=config['messages']['email_success']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def invalid_email(config):
    embed = discord.Embed(
        color=discord.Color.red(),
        title=config['messages']['invalid_email']['title'],
        description=config['messages']['invalid_email']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def email_timeout(config):
    embed = discord.Embed(
        color=discord.Color.red(),
        title=config['messages']['email_timeout']['title'],
        description=config['messages']['email_timeout']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def email_in_use(config):
    embed = discord.Embed(
        color=discord.Color.red(),
        title=config['messages']['email_in_use']['title'],
        description=config['messages']['email_in_use']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def dm_cancelled(config):
    embed = discord.Embed(
        color=discord.Color.red(),
        title=config['messages']['dm_cancelled']['title'],
        description=config['messages']['dm_cancelled']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def delete_account(config):
    embed = discord.Embed(
        color=discord.Color.red(),
        title=config['messages']['delete_account']['title'],
        description=config['messages']['delete_account']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def delete_account_admin(config):
    embed = discord.Embed(
        color=discord.Color.green(),
        title=config['messages']['delete_account_admin']['title'],
        description=config['messages']['delete_account_admin']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def database_content(db_content, config):
    embed = discord.Embed(
        color=discord.Color.dark_grey(),
        title=config['messages']['database_content']['title'],
        description=f"{config['messages']['database_content']['message']}{db_content}"
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def welcome_message(config):
    embed = discord.Embed(
        color=discord.Color.green(),
        title=config['messages']['welcome_message']['title'],
        description=config['messages']['welcome_message']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def in_progress(config):
    embed = discord.Embed(
        color=discord.Color.orange(),
        title=config['messages']['trial_in_progress']['title'],
        description=config['messages']['trial_in_progress']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def end_trial(config):
    embed = discord.Embed(
        color=discord.Color.red(),
        title=config['messages']['end_trial']['title'],
        description=config['messages']['end_trial']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def already_tested(config):
    embed = discord.Embed(
        color=discord.Color.red(),
        title=config['messages']['already_tested']['title'],
        description=config['messages']['already_tested']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def never_tested(config):
    embed = discord.Embed(
        color=discord.Color.red(),
        title=config['messages']['never_tested']['title'],
        description=config['messages']['never_tested']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def unauthorized(config):
    embed = discord.Embed(
        color=discord.Color.red(),
        title=config['messages']['unauthorized']['title'],
        description=config['messages']['unauthorized']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def launch_trial(config):
    embed = discord.Embed(
        color=discord.Color.green(),
        title=config['messages']['launch_trial']['title'],
        description=config['messages']['launch_trial']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def not_in_db(config):
    embed = discord.Embed(
        color=discord.Color.red(),
        title=config['messages']['not_in_db']['title'],
        description=config['messages']['not_in_db']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def reset_trial(config):
    embed = discord.Embed(
        color=discord.Color.green(),
        title=config['messages']['reset_trial']['title'],
        description=config['messages']['reset_trial']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def confirm_send_welcome(config):
    embed = discord.Embed(
        color=discord.Color.green(),
        title=config['messages']['confirm_send_welcome']['title'],
        description=config['messages']['confirm_send_welcome']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def test_message(config, title, description):
    embed = discord.Embed(
        color=discord.Color.green(),
        title=title,
        description=description
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def subscription_in_progress(config):
    embed = discord.Embed(
        color=discord.Color.green(),
        title=config['messages']['subscription_in_progress']['title'],
        description=config['messages']['subscription_in_progress']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def subscription1(config):
    embed = discord.Embed(
        color=discord.Color.green(),
        title=config['messages']['subscription1']['title'],
        description=config['messages']['subscription1']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def subscription2(config):
    embed = discord.Embed(
        color=discord.Color.green(),
        title=config['messages']['subscription2']['title'],
        description=config['messages']['subscription2']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def select_lib_timeout(config):
    embed = discord.Embed(
        color=discord.Color.red(),
        title=config['messages']['select_lib_timeout']['title'],
        description=config['messages']['select_lib_timeout']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def current_subscriptions(subscriptions, config):
    embed = discord.Embed(
        color=discord.Color.green(),
        title=config['messages']['current_subscriptions']['title'],
        description=f"{config['messages']['current_subscriptions']['message']}{subscriptions}"
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def pre_end_subscription(config):
    embed = discord.Embed(
        color=discord.Color.green(),
        title=config['messages']['pre_end_subscription']['title'],
        description=config['messages']['pre_end_subscription']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def end_subscription(config):
    embed = discord.Embed(
        color=discord.Color.green(),
        title=config['messages']['end_subscription']['title'],
        description=config['messages']['end_subscription']['message']
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def private_new_trial(config, member):
    desc = config['messages']['private_new_trial']['message'].replace('<member>', str(member))
    embed = discord.Embed(
        color=discord.Color.green(),
        title=f"{config['messages']['private_new_trial']['title']}",
        description=desc
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def private_new_subscription(config, member):
    desc = config['messages']['private_new_subscription']['message'].replace('<member>', str(member))
    embed = discord.Embed(
        color=discord.Color.green(),
        title=f"{config['messages']['private_new_subscription']['title']}",
        description=desc
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed


async def private_end_subscription(config, member):
    desc = config['messages']['private_end_subscription']['message'].replace('<member>', str(member))
    embed = discord.Embed(
        color=discord.Color.green(),
        title=f"{config['messages']['private_end_subscription']['title']}",
        description=desc
    )
    embed.set_thumbnail(url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png")
    embed.set_footer(icon_url="https://web.maison-jo.synology.me/images/PlexFriendsLogo.png",
                     text=f"PlexFriends - v{config['version']}")
    return embed
