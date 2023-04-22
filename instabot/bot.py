import time
import logging
import random

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/bot.log")
    ]
)

logger = logging.getLogger()

def unfollow_users(cl, users_to_unfollow, config):
    unfollow_interval = config['unfollow_interval']
    for user in users_to_unfollow:
        time.sleep(random.randint(unfollow_interval[0], unfollow_interval[1]))
        cl.user_unfollow(user)
        logger.info(f"Unfollowed user {user.username}")

def follow_users(cl, SOURCE_ACCOUNT, FOLLOWS_PER_DAY):
    logger.info("Started following process..")

    user_id = cl.user_id_from_username(SOURCE_ACCOUNT)

    average_sleep_time = 86400 / FOLLOWS_PER_DAY
    min_sleep_time = average_sleep_time * 0.5  # 50% less than the average
    max_sleep_time = average_sleep_time * 1.5  # 50% more than the average

    users = cl.user_followers(user_id, True, FOLLOWS_PER_DAY)

    for user in users:
        cl.user_follow(user)
        logger.info(f"Followed user {user}")
        sleep_time = random.uniform(min_sleep_time, max_sleep_time)
        logger.info(f"Sleeping for {sleep_time} seconds before following {user}")
        time.sleep(sleep_time)
