import json
import logging
import os


def locate(location):
    """
    Verifies the presence of a config.ini file
    :param location : Full data file link as /volume/config.json (docker volume format)
    :return : Exact path where the data file is available, none if unavailable
    """
    if os.path.isfile(location):
        return location.replace('config.json', '')
    location2 = location[1:]
    if os.path.isfile(location2):
        return location2.replace('config.json', '')
    return None


def generate_empty_config():
    config = {
        "bot_token": "",
        "guild_id": 0,
        "private_channel_id": 0,
        "role_subscriber": "",
        "plex_user": "",
        "plex_password": "",
        "plex_url": "",
        "plex_token": "",
        "overseerr_url": "",
        "overseerr_api_key": "",
        "test_duration": 0
    }

    try:
        with open('/config/config.json', 'w') as file:
            json.dump(config, file, indent=4)
        return True
    except:
        try:
            with open('config/config.json', 'w') as file:
                json.dump(config, file, indent=4)
            return True
        except:
            logging.error("INIT: Error while creating config.json file. Inaccessible config folder !")
            return False


def locate_generate_empty_members(link_config):
    if os.path.isfile(f'{link_config}members.json'):
        return f'{link_config}members.json'

    try:
        fichier = open(f'{link_config}members.json', "w")
        fichier.write("{}")
        fichier.close()
        return f'{link_config}members.json'
    except:
        logging.error("INIT: Error while creating members.json file. Inaccessible config folder !")
        return None


def locate_generate_trial_subscription(link_config):
    if os.path.isfile(f'{link_config}trial.json'):
        return f'{link_config}trial.json'

    try:
        fichier = open(f'{link_config}trial.json', "w")
        fichier.write("{}")
        fichier.close()
        return f'{link_config}trial.json'
    except:
        logging.error("INIT: Error while creating trial.json file. Inaccessible config folder !")
        return None


def locate_generate_history_transactions(link_config):
    if os.path.isfile(f'{link_config}history_transactions.json'):
        return f'{link_config}history_transactions.json'

    try:
        fichier = open(f'{link_config}history_transactions.json', "w")
        fichier.write("[]")
        fichier.close()
        return f'{link_config}history_transactions.json'
    except:
        logging.error("INIT: Error while creating history_transactions.json file. Inaccessible config folder !")
        return None


def locate_generate_subscription(link_config):
    if os.path.isfile(f'{link_config}subscription.json'):
        return f'{link_config}subscription.json'

    try:
        fichier = open(f'{link_config}subscription.json', "w")
        fichier.write("{}")
        fichier.close()
        return f'{link_config}subscription.json'
    except:
        logging.error("INIT: Error while creating subscription.json file. Inaccessible config folder !")
        return None
