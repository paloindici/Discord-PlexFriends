import json
import os
from datetime import datetime

from dateutil.relativedelta import relativedelta


def init_language(link_config):
    messages = {}
    personal_messages = {}
    link_default_message = link_config.replace("config/", "default_messages.json")
    with open(link_default_message, encoding='utf-8') as outfile:
        messages = json.load(outfile)
    link_personal_message = link_config + "language.json"
    if os.path.isfile(link_personal_message):
        with open(link_personal_message, encoding='utf-8') as outfile:
            personal_messages = json.load(outfile)
        for subject in messages:
            if subject in personal_messages:
                for section in personal_messages[subject]:
                    messages[subject][section] = personal_messages[subject][section]
    return messages


def read_config(link_config):
    with open(link_config) as outfile:
        config = json.load(outfile)
    return config


def add_member(member_link, member_id, member_email):
    with open(member_link) as outfile:
        members = json.load(outfile)
    members[member_id] = member_email
    with open(member_link, "w") as outfile:
        json.dump(members, outfile, indent=4)


def delete_member(member_link, member_id):
    with open(member_link) as outfile:
        members = json.load(outfile)
    if member_id in members:
        del members[member_id]
        with open(member_link, "w") as outfile:
            json.dump(members, outfile, indent=4)
            return True
    else:
        return False


def read_member(member_link):
    with open(member_link) as outfile:
        return json.load(outfile)


def read_trial(trial_link):
    with open(trial_link) as outfile:
        return json.load(outfile)


def write_trial(trial_link, member_id, value):
    with open(trial_link) as outfile:
        trial = json.load(outfile)
    trial[str(member_id)] = value
    with open(trial_link, "w") as outfile:
        json.dump(trial, outfile, indent=4)


def delete_trial(trial_link, member_id):
    with open(trial_link) as outfile:
        members = json.load(outfile)
    if member_id in members:
        del members[member_id]
        with open(trial_link, "w") as outfile:
            json.dump(members, outfile, indent=4)
            return True
    else:
        return False


def write_history_transactions(history_link, transaction):
    with open(history_link) as outfile:
        transac = json.load(outfile)
    transac.append(transaction)
    with open(history_link, "w") as outfile:
        json.dump(transac, outfile, indent=4)


def read_history_transactions(history_link):
    with open(history_link) as outfile:
        return json.load(outfile)


def write_subscription(subscription_link, member_id):
    with open(subscription_link) as outfile:
        subscription = json.load(outfile)
    if member_id in subscription:
        if subscription[member_id] == 0:
            date_time = datetime.today() + relativedelta(months=1)
        else:
            old_datetime = datetime.fromtimestamp(subscription[member_id])
            date_time = old_datetime + relativedelta(months=1)
    else:
        date_time = datetime.today() + relativedelta(months=1)
    subscription[member_id] = int(datetime.timestamp(date_time))
    with open(subscription_link, "w") as outfile:
        json.dump(subscription, outfile, indent=4)


def write_end_subscription(subscription_link, member_id):
    with open(subscription_link) as outfile:
        subscription = json.load(outfile)
    subscription[member_id] = 0
    with open(subscription_link, "w") as outfile:
        json.dump(subscription, outfile, indent=4)


def read_subscription(subscription_link):
    with open(subscription_link) as outfile:
        return json.load(outfile)
