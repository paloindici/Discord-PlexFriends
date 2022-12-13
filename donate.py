import json
import logging

import requests

base_url = 'https://donatebot.io/api/v1/donations/'


def build_headers(donate_api):
    headers = {
        "Authorization": donate_api,
        "User-Agent": 'Donate-Bot-PlexFriends/1.0.3'
    }
    return headers


def new_donation(donate_api, discord_server, find='Completed'):
    response = requests.get(f'{base_url}{discord_server}/new?find={find}',
                            headers=build_headers(donate_api))
    if response.status_code == 200:
        result = json.loads(response.text)
        return result
    return None


def ended_subscriptions(donate_api, discord_server):
    response = requests.get(f'{base_url}{discord_server}/endedsubscriptions',
                            headers=build_headers(donate_api))
    if response.status_code == 200:
        result = json.loads(response.text)
        return result
    return None


def mark_processed(donate_api, discord_server, transaction_id, isEndedSubscription=False, markProcessed=True):
    response = requests.post(f'{base_url}{discord_server}/{transaction_id}/mark?isEndedSubscription={isEndedSubscription}&markProcessed={markProcessed}',
                             headers=build_headers(donate_api))
    if response.status_code == 200:
        logging.info(f"DONATE: Transaction ID {transaction_id} mark as processed.")
        return True
    elif response.status_code == 404:
        logging.info(f"DONATE: Transaction ID not found: {transaction_id}.")
        return False
    return None
