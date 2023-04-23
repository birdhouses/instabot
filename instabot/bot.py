import time
import logging
import random
import datetime

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/bot.log")
    ]
)

logger = logging.getLogger()

def save_followed_user(user_id):
    with open("followed_users.txt", "a") as file:
        file.write(f"{user_id},{datetime.datetime.now()}\n")

def load_followed_users():
    followed_users = []

    with open("followed_users.txt", "r") as file:
        for line in file:
            user_id, timestamp = line.strip().split(",")
            followed_users.append((int(user_id), datetime.datetime.fromisoformat(timestamp)))

    return followed_users

def filter_users_to_unfollow(followed_users, follow_time):
    now = datetime.datetime.now()
    return [user for user, timestamp in followed_users if (now - timestamp).total_seconds() >= follow_time]

def remove_unfollowed_user(user):
    followed_users = load_followed_users()
    followed_users.remove(user)

    with open("followed_users.txt", "w") as file:
        for user in followed_users:
            file.write(f"{user}\n")


def unfollow_users(cl, config):
    logger.info("Started unfollowing process")
    unfollow_after = config['unfollow_after']
    followed_users = load_followed_users()
    users_to_unfollow = filter_users_to_unfollow(followed_users, unfollow_after)
    unfollow_users_count = len(users_to_unfollow)
    logger.info(f"Going to unfollow {unfollow_users_count} users")
    for user in users_to_unfollow:
        sleep_time = random.uniform(300, 900)
        logger.info(f"Sleeping for {sleep_time} before unfollowing {user}")
        time.sleep(sleep_time)
        cl.user_unfollow(user)
        logger.info(f"Unfollowed user {user.username}")
        remove_unfollowed_user(user)

def follow_users(cl, SOURCE_ACCOUNT, FOLLOWS_PER_DAY):
    logger.info("Started following process..")

    user_id = cl.user_id_from_username(SOURCE_ACCOUNT)

    average_sleep_time = 86400 / FOLLOWS_PER_DAY
    min_sleep_time = average_sleep_time * 0.5  # 50% less than the average
    max_sleep_time = average_sleep_time * 1.5  # 50% more than the average

    users = cl.user_followers(user_id, True, FOLLOWS_PER_DAY)

    for user in users:
        logger.info(f"Following user: {user}")
        cl.user_follow(user)
        sleep_time = random.uniform(min_sleep_time, max_sleep_time)
        save_followed_user(user)
        logger.info(f"Sleeping for {sleep_time} seconds before following next user..")
        time.sleep(sleep_time)
