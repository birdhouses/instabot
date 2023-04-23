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
from typing import Union
import time
import json
import uuid
import os
import logging

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

def update_client_settings(client: Client, settings: dict) -> bool:
    return client.set_settings(settings)


def rebuild_client_settings(client: Client) -> dict:
    # Get the current settings
    current_settings = client.settings

    # Generate new settings using the custom generate_new_settings function
    new_settings = generate_new_settings(current_settings)

    # Update the client's settings with the new values
    client.settings = new_settings

    # Save the new settings using the update_client_settings function
    update_client_settings(client, new_settings)

    return new_settings

def generate_new_settings(existing_settings: dict) -> dict:
    new_uuids = {
        "phone_id": str(uuid.uuid4()),
        "uuid": str(uuid.uuid4()),
        "client_session_id": str(uuid.uuid4()),
        "advertising_id": str(uuid.uuid4()),
        "android_device_id": existing_settings["uuids"]["android_device_id"],
        "request_id": str(uuid.uuid4()),
        "tray_session_id": str(uuid.uuid4())
    }

    new_settings = {
        "uuids": new_uuids,
        "mid": existing_settings["mid"],
        "ig_u_rur": existing_settings["ig_u_rur"],
        "ig_www_claim": existing_settings["ig_www_claim"],
        "authorization_data": existing_settings["authorization_data"],
        "cookies": existing_settings["cookies"],
        "last_login": existing_settings["last_login"],
        "device_settings": existing_settings["device_settings"],
        "user_agent": existing_settings["user_agent"],
        "country": existing_settings["country"],
        "country_code": existing_settings["country_code"],
        "locale": existing_settings["locale"],
        "timezone_offset": existing_settings["timezone_offset"]
    }

    return new_settings

def freeze(message: str, hours: int = 0, days: int = 0) -> None:
    print(f"Freezing due to: {message}")
    freeze_time = hours * 3600 + days * 86400
    time.sleep(freeze_time)

def next_proxy() -> str:
    return "http://riccmpgq:nu5x1biz04h9@45.94.47.66:8110"


def get_client(username: str, password: str) -> Union[Client, None]:
    settings_folder = "settings"
    os.makedirs(settings_folder, exist_ok=True)
    session_file_path = os.path.join(settings_folder, f"settings_{username}.json")

    def handle_exception(client: Client, e: Exception) -> Union[bool, None]:
        nonlocal username, password
        if isinstance(e, BadPassword):
            logger.exception(e)
            client.set_proxy(next_proxy().href)
            if client.relogin_attempt > 0:
                freeze(str(e), days=7)
                raise ReloginAttemptExceeded(e)

            return update_client_settings(client, client.get_settings())

        elif isinstance(e, LoginRequired):
            logger.exception(e)
            client.login(username, password)
            return update_client_settings(client, client.get_settings())
        elif isinstance(e, ChallengeRequired):
            api_path = client.last_json.get("challenge", {}).get("api_path")
            if api_path == "/challenge/":
                client.set_proxy(next_proxy().href)
                client.settings = rebuild_client_settings()
            else:
                try:
                    client.challenge_resolve(client.last_json)
                except ChallengeRequired as e:
                    freeze("Manual Challenge Required", days=2)
                    raise e
                except (
                    ChallengeRequired,
                    SelectContactPointRecoveryForm,
                    RecaptchaChallengeForm,
                ) as e:
                    freeze(str(e), days=4)
                    raise e
                update_client_settings(client.get_settings())
            return True
        elif isinstance(e, FeedbackRequired):
            message = client.last_json["feedback_message"]
            if "This action was blocked. Please try again later" in message:
                freeze(message, hours=12)
            elif "We restrict certain activity to protect our community" in message:
                freeze(message, hours=12)
            elif "Your account has been temporarily blocked" in message:
                freeze(message)
        raise e

    cl = Client()

    if os.path.exists(session_file_path):
        cl.load_settings(session_file_path)
        try:
            cl.get_timeline_feed()  # Check if the session is valid
            logger.info("Session is valid, login with session")

        except Exception as e:
            logger(f"Session is invalid: {e}")
            os.remove(session_file_path)
            cl.login(username, password)
            cl.dump_settings(session_file_path)
            logger.info("Session saved to file")
    else:
        cl.login(username, password)
        cl.dump_settings(session_file_path)
        logger.info("Session saved to file")

    cl.handle_exception = handle_exception
    cl.set_proxy(next_proxy())

    return cl