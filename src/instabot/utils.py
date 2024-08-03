from instagrapi import Client
from instagrapi.exceptions import (
    BadPassword,
    ChallengeRequired,
    FeedbackRequired,
    LoginRequired,
    PleaseWaitFewMinutes,
    RecaptchaChallengeForm,
    ReloginAttemptExceeded,
    SelectContactPointRecoveryForm
)
from instagrapi.types import Media
from requests.exceptions import RetryError
from typing import Union, List
import time
import json
import os
import os.path
import logging
import random
from dateutil import parser
import asyncio
import instagrapi
from PIL import Image

logs_dir = "./artifacts/logs/"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(logs_dir + "bot.log")
    ]
)
### Logger used throughout the entire project
logger = logging.getLogger()

def get_approximate_sleep_time(days=0, hours=0, minutes=0) -> int:
    total_seconds =  days * 86400 + hours * 3600 + minutes * 60
    min_time = total_seconds * 0.5
    max_time = total_seconds * 1.5

    return random.uniform(min_time, max_time)

def convert_webp_to_jpg(image_path, output_path):
    """Converts a WEBP image to JPG."""
    try:
        Image.open(image_path).convert("RGB").save(output_path, "JPEG")
        logger.info(f"Converted WEBP to JPG: {output_path}")
    except Exception as e:
        logger.error(f"Error converting WEBP to JPG for {image_path}: {e}")
        raise

def convert_png_to_jpg(image_path, output_path):
    """Converts a PNG image to JPG."""
    try:
        Image.open(image_path).convert("RGB").save(output_path, "JPEG")
        logger.info(f"Converted PNG to JPG: {output_path}")
    except Exception as e:
        logger.error(f"Error converting PNG to JPG for {image_path}: {e}")
        raise

def load_config(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)

async def freeze(message: str, hours: int = 0, days: int = 0) -> None:
    print(f"Freezing due to: {message}")
    freeze_time = hours * 3600 + days * 86400
    await asyncio.sleep(freeze_time)

def read_proxies():
    try:
        with open('../proxies.txt', 'r') as f:
            raw_proxies = [line.strip() for line in f.readlines()]
            return raw_proxies
    except FileNotFoundError:
        print("Warning: proxies.txt not found, returning an empty list.")
        return []

def next_proxy() -> str:
    raw_proxies = read_proxies()

    if not raw_proxies:
        print("No proxies available, returning an empty string.")
        return ""

    raw_proxy = random.choice(raw_proxies)

    ip, port, username, password = raw_proxy.split(':')
    formatted_proxy = f"http://{username}:{password}@{ip}:{port}"

    return formatted_proxy


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
    if os.path.exists(session_file_path):
        try:
            os.remove(session_file_path)
            logger.info(f"Session file removed: {session_file_path}")
        except OSError as e:
            logger.warning(f"Error removing session file: {e}")
    else:
        logger.warning(f"Session file not found: {session_file_path}")

    login_and_save_session(client, username, password, session_file_path)

def login_and_save_session(client, username, password, session_file_path):
    client.login(username, password)
    client.dump_settings(session_file_path)
    logger.info("Session saved to file")

async def get_client(account) -> Union[Client, None]:
    username = account['account_details']['username']
    password = account['account_details']['password']
    use_proxy = account['use_proxies']['use_proxy']

    settings_folder = "./artifacts/settings"
    os.makedirs(settings_folder, exist_ok=True)
    session_file_path = os.path.join(settings_folder, f"settings_{username}.json")

    async def handle_exception(client: Client, e: Exception) -> Union[bool, None]:
        logger.warning(f"Error while logging in: {e}")
        if isinstance(e, BadPassword):
            logger.error(f"Login failed for user {username}: {e}")
            return None
        elif isinstance(e, LoginRequired):
            remove_session_and_login(client, username=username, password=password, session_file_path=session_file_path)
            return True
        elif isinstance(e, ChallengeRequired):
            raise e
        elif isinstance(e, FeedbackRequired):
            switchproxy(client, use_proxy=use_proxy)

            await freeze(e, hours=1)
            remove_session_and_login(client, username=username, password=password, session_file_path=session_file_path)
            return True
        elif isinstance(e, PleaseWaitFewMinutes):
            switchproxy(client, use_proxy=use_proxy)
            await freeze(e, 1)
            return True
        elif isinstance(e, RetryError):
            switchproxy(client, use_proxy=use_proxy)
            await freeze(e, 1)
            remove_session_and_login(client, username=username, password=password, session_file_path=session_file_path)
            return True
        else:
            retry_count = 1
            freeze_time = retry_count * 4

            freeze(e, freeze_time)

            if retry_count < 3:
                raise e

    client = Client()

    switchproxy(client, use_proxy=use_proxy)

    client.handle_exception = handle_exception
    load_or_login_and_save_session(client, username, password, session_file_path)

    return client

def switchproxy(client: Client, use_proxy: bool) -> None:
    if use_proxy:
        print(use_proxy)
        client.set_proxy(next_proxy())
    else:
        return

def get_user_id(cl: Client, source_account: str) -> int:
    return cl.user_id_from_username(source_account)

def get_followers(cl: Client, user_id: int, amount: int) -> List[str]:
    return cl.user_followers(user_id, True, amount=amount)

def calculate_sleep_time(actions_per_day: int) -> float:
    average_sleep_time = 86400 / actions_per_day
    min_sleep_time = average_sleep_time * 0.9
    max_sleep_time = average_sleep_time * 1.2
    return random.uniform(min_sleep_time, max_sleep_time)

def parse_time_string(time_string: str) -> int:
    """Parse the time string in the format 'day-hour-min-s' into total seconds."""
    parts = time_string.split('-')
    days, hours, minutes, seconds = [int(part) for part in parts]
    total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
    return total_seconds