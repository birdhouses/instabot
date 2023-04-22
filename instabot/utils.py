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

def load_config(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def update_client_settings(settings: dict) -> None:
    # Implement the function to update the client settings.
    pass

def rebuild_client_settings() -> dict:
    # Implement the function to rebuild the client settings.
    pass

def freeze(message: str, hours: int = 0, days: int = 0) -> None:
    print(f"Freezing due to: {message}")
    freeze_time = hours * 3600 + days * 86400
    time.sleep(freeze_time)


def get_client(username: str, password: str) -> Union[Client, None]:
    def handle_exception(client: Client, e: Exception) -> Union[bool, None]:
        nonlocal username, password
        if isinstance(e, BadPassword):
            client.logger.exception(e)
            raise ReloginAttemptExceeded(e)

        elif isinstance(e, LoginRequired):
            client.logger.exception(e)
            client.login(username, password)
            return update_client_settings(client.get_settings())
        elif isinstance(e, ChallengeRequired):
            api_path = client.last_json.get("challenge", {}).get("api_path")
            if api_path == "/challenge/":

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
    cl.handle_exception = handle_exception
    cl.login(username, password)
    return cl