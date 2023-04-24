from instagrapi import Client
from instagrapi.exceptions import (
    BadPassword,
    ChallengeRequired,
    FeedbackRequired,
    LoginRequired,
    PleaseWaitFewMinutes,
    RecaptchaChallengeForm,
    ReloginAttemptExceeded,
    SelectContactPointRecoveryForm,
)
from requests.exceptions import RetryError
from typing import Union, List
import time
import json
import os
import logging
import random
import requests

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/bot.log")
    ]
)
logger = logging.getLogger()


def load_config(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def freeze(message: str, hours: int = 0, days: int = 0) -> None:
    print(f"Freezing due to: {message}")
    freeze_time = hours * 3600 + days * 86400
    time.sleep(freeze_time)

def next_proxy() -> str:
    config = load_config('config.json')
    url = config['proxy_url']
    response = requests.get(url)
    response.raise_for_status()

    raw_proxies = response.text.strip().split('\n')
    proxies = [f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}" for proxy in raw_proxies]

    return random.choice(proxies)

def load_or_login_and_save_session(client, username, password, session_file_path):
    if os.path.exists(session_file_path):
        client.load_settings(session_file_path)

        try:
            client.get_timeline_feed()  # Check if the session is valid
            logger.info("Session is valid, login with session")

        except Exception as e:
            logger.warning(f"Session is invalid: {e}")
            remove_session_and_login(client, username, password, session_file_path)
    else:
        login_and_save_session(client, username, password, session_file_path)

def remove_session_and_login(client, username, password, session_file_path):
    try:
        os.remove(session_file_path)
    except OSError as e:
        logger.warning(f"Error removing session file: {e}")

    login_and_save_session(client, username, password, session_file_path)

def login_and_save_session(client, username, password, session_file_path):
    client.login(username, password)
    client.dump_settings(session_file_path)
    logger.info("Session saved to file")

def get_client(username: str, password: str) -> Union[Client, None]:
    settings_folder = "settings"
    os.makedirs(settings_folder, exist_ok=True)
    session_file_path = os.path.join(settings_folder, f"settings_{username}.json")

    def handle_exception(client: Client, e: Exception) -> Union[bool, None]:
        if isinstance(e, BadPassword):
            raise e
        elif isinstance(e, LoginRequired):
            freeze(e, 1)
            remove_session_and_login(client, username=username, password=password, session_file_path=session_file_path)
            return True
        elif isinstance(e, ChallengeRequired):
            raise e
        elif isinstance(e, FeedbackRequired):
            freeze(e, hours=1)
            remove_session_and_login(client, username=username, password=password, session_file_path=session_file_path)
            return True
        elif isinstance(e, PleaseWaitFewMinutes):
            freeze(e, 1)
            return True
        elif isinstance(e, RetryError):
            remove_session_and_login(client, username=username, password=password, session_file_path=session_file_path)
            freeze(e, hours=1)
            return True
        raise e

    client = Client()
    client.handle_exception = handle_exception
    load_or_login_and_save_session(client, username, password, session_file_path)

    return client

def get_user_id(cl: Client, source_account: str) -> int:
    return cl.user_id_from_username(source_account)

def get_followers(cl: Client, user_id: int, amount: int) -> List[str]:
    return cl.user_followers(user_id, True, amount=amount)

def calculate_sleep_time(min_sleep_time: float, max_sleep_time: float) -> float:
    return random.uniform(min_sleep_time, max_sleep_time)