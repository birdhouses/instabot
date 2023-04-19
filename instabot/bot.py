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

def follow_users(cl, config, followers):
    follow_interval = config['follow_interval']
    followed_users = []
    for i, user in enumerate(followers):
        time.sleep(random.randint(follow_interval[0], follow_interval[1]))
        logger.info(f"Followed user {user}")
        cl.user_follow(user)
        followed_users.append(user)

    return followed_users