import instabot
import time
import logging
from instagrapi import Client

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/bot.log")
    ]
)
logger = logging.getLogger()

if __name__ == "__main__":
    config = instabot.load_config('config.json')

    ACCOUNT_USERNAME = config['account']['username']
    ACCOUNT_PASSWORD = config['account']['password']
    SOURCE_ACCOUNT = config['source_account']
    FOLLOWS_PER_DAY = config['follows_per_day']

    cl = instabot.get_client(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

    while True:
        instabot.follow_users(cl, SOURCE_ACCOUNT, FOLLOWS_PER_DAY)
