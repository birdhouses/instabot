import time
import logging
import random
import datetime
from instagrapi import Client
from typing import Any, List, Tuple, Dict
import os
from .like_media import like_recent_posts
import threading
from .utils import load_config

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/bot.log")
    ]
)

logger = logging.getLogger()

def save_followed_user(cl: Client, user_id: int) -> None:
    """Save followed user ID and timestamp to a file."""
    followed_users_folder = "followed_users"
    os.makedirs(followed_users_folder, exist_ok=True)
    file_path = os.path.join(followed_users_folder, f"followed_users_{cl.user_id}.txt")

    with open(file_path, "a") as file:
        file.write(f"{user_id},{datetime.datetime.now()}\n")

def load_followed_users(cl: Client) -> List[Tuple[int, datetime.datetime]]:
    """Load followed users' IDs and timestamps from a file."""
    followed_users = []
    followed_users_folder = "followed_users"
    os.makedirs(followed_users_folder, exist_ok=True)
    file_path = os.path.join(followed_users_folder, f"followed_users_{cl.user_id}.txt")

    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            pass

    with open(file_path, "r") as file:
        for line in file:
            user_id, timestamp = line.strip().split(",")
            followed_users.append((int(user_id), datetime.datetime.fromisoformat(timestamp)))

    return followed_users

def filter_users_to_unfollow(followed_users: List[Tuple[int, datetime.datetime]], follow_time: int) -> List[int]:
    """Filter users that should be unfollowed based on follow_time."""
    now = datetime.datetime.now()
    return [user for user, timestamp in followed_users if (now - timestamp).total_seconds() >= follow_time]

def remove_unfollowed_user(cl: Client, user: int) -> None:
    """Remove unfollowed user from the followed users file."""
    followed_users = load_followed_users(cl)
    followed_users.remove(user)

    followed_users_folder = "followed_users"
    os.makedirs(followed_users_folder, exist_ok=True)
    file_path = os.path.join(followed_users_folder, f"followed_users_{cl.user_id}.txt")

    with open(file_path, "w") as file:
        for user in followed_users:
            file.write(f"{user}\n")

def unfollow_users(cl: Client, unfollow_after: int) -> None:
    """Unfollow users after a specified time."""
    logger.info("Started unfollowing process")
    followed_users = load_followed_users(cl)
    users_to_unfollow = filter_users_to_unfollow(followed_users, follow_time=unfollow_after)
    unfollow_users_count = len(users_to_unfollow)
    logger.info(f"Going to unfollow {unfollow_users_count} users")
    for user in users_to_unfollow:
        sleep_time = random.uniform(300, 900)
        logger.info(f"Sleeping for {sleep_time} before unfollowing {user}")
        time.sleep(sleep_time)
        cl.user_unfollow(user)
        logger.info(f"Unfollowed user {user}")

def user_not_followed_before(cl: Client, user_id: int) -> bool:
    """Check if the given user_id has been followed before."""
    followed_users = load_followed_users(cl)
    for user, _ in followed_users:
        if user == user_id:
            return False
    return True

def follow_user(cl: Client, user_id: int, engagement: Dict[str, Any]) -> bool:
    """Follow a user and add it to followed_users file."""

    if user_not_followed_before(cl, user_id):
        cl.user_follow(user_id)
        save_followed_user(cl, user_id=user_id)

        if engagement["like_recent_posts"]:
            like_recent_posts(cl, user_id=user_id, engagement=engagement)

        logger.info(f"Followed user: {user_id}")

        return True
    logger.info("User was followed before, skipped")

    return False


def follow_user_followers(cl: Client, source_account: str, follows_per_day: int, engagement: Dict[str, Any]) -> None:
    """Follow the followers of the source account and engage with their content."""
    logger.info("Started following user followers process..")

    user_id = cl.user_id_from_username(source_account)
    average_sleep_time = 86400 / follows_per_day
    min_sleep_time = average_sleep_time * 0.5
    max_sleep_time = average_sleep_time * 1.5

    users = cl.user_followers(user_id, True, amount=follows_per_day)

    for user in users:
        try:
            sleep_time = random.uniform(min_sleep_time, max_sleep_time)
            if follow_user(cl, user, engagement):
                logger.info(f"Sleeping for {sleep_time} seconds before following next user..")
                time.sleep(sleep_time)

        except Exception as e:
            logger.error(f"Error while processing user {user}: {e}")
            continue