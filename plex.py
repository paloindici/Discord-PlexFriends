import logging
import time

from plexapi.exceptions import BadRequest, NotFound
from plexapi.myplex import MyPlexAccount


def plex_login(user, password):
    logging.info(f"PLEXAPI: Logging into Account: {user}")
    success = False
    while not success:
        try:
            plex_account = MyPlexAccount(user, password)
            success = True
        except BadRequest as e:
            logging.error(f"PLEXAPI: Login to account: {user} failed with status: {e}, retrying in 30sec")
            time.sleep(30)
    logging.info(f"PLEXAPI: Logged in!")
    return plex_account


def add_user(plex_account, user_email, plex_server, sections):
    try:
        logging.info(f"PLEXAPI: Inviting {user_email} to {plex_server.friendlyName}")
        plex_account.inviteFriend(user=user_email, server=plex_server, sections=sections)
        logging.info(f"PLEXAPI: Invited {user_email} to {plex_server.friendlyName}")
        return True
    except BadRequest:
        logging.error(f'PLEXAPI: Already sharing with {user_email} on server {plex_server.friendlyName}')
        return False


def remove_user(plex_account, user_email):
    try:
        logging.info(f"PLEXAPI: Removing {user_email} from shares on account: {plex_account.email}")
        plex_account.removeFriend(user_email)
        logging.info(f"PLEXAPI: Removed {user_email} from shares on account: {plex_account.email}")
        return True
    except NotFound:
        logging.error(
            f"PLEXAPI: Cannot remove {user_email} from shares on account: {plex_account.email}: not sharing with this user")
        return False
    except Exception as e:
        logging.error(
            f"PLEXAPI: Cannot remove {user_email} from shares on account: {plex_account.email} due to unhandled exception: {e}")
        return False


def remove_user_pending(plex_account, user_email):
    try:
        logging.info(f"PLEXAPI: Removing {user_email} from shares on account: {plex_account.email}")
        plex_account.cancelInvite(user_email)
        logging.info(f"PLEXAPI: Removed {user_email} from shares on account: {plex_account.email}")
        return True
    except NotFound:
        logging.error(
            f"PLEXAPI: Cannot remove {user_email} from shares on account: {plex_account.email}: not sharing with this user")
        return False
    except Exception as e:
        logging.error(
            f"PLEXAPI: Cannot remove {user_email} from shares on account: {plex_account.email} due to unhandled exception: {e}")
        return False


def update_friend(plex_account, user_email, plex_server, library):
    try:
        logging.info(f"PLEXAPI: Update friend {user_email} with library: {library}")
        if not library:
            plex_account.updateFriend(user_email, plex_server, None, removeSections=True)
        else:
            plex_account.updateFriend(user_email, plex_server, sections=library)
        return True
    except NotFound:
        logging.error(
            f"PLEXAPI: Cannot update {user_email} from shares on account: "
            f"{plex_account.email}: not sharing with this user")
        return False


def select_library(bot_name, plex_server, roles):
    list_roles = []
    list_sections = []
    for role in roles:
        if len(str(role)) > len(bot_name):
            if str(role)[:len(bot_name)] == bot_name:
                list_roles.append(str(role)[len(bot_name) + 3:])
    sections = plex_server.library.sections()
    for section in sections:
        if section.title in list_roles:
            list_sections.append(section)
    print(f"Selection des library: {list_sections}")
    return list_sections


def is_friends(user_email, plex_account):
    plex_exist_users = plex_account.users()
    for plex_exist_user in plex_exist_users:
        if str(plex_exist_user.email) == user_email:
            return True
    return False


def is_pending(user_email, plex_account):
    plex_pending_users = plex_account.pendingInvites(includeSent=True, includeReceived=False)
    for plex_pending_user in plex_pending_users:
        if str(plex_pending_user.email) == user_email:
            return True
    return False


def all_users(plex_account):
    return plex_account.users()
