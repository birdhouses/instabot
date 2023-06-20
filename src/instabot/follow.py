import time
import logging
import random
import datetime
from instagrapi import Client
from typing import Any, List, Tuple, Dict
import os
import asyncio
import instabot
from instabot import utils
from instabot import like

followed_users_folder = "./artifacts/logs/followed_users"

def save_followed_user(cl: Client, user_id: int) -> None:
    """Save followed user ID and timestamp to a file."""

    os.makedirs(followed_users_folder, exist_ok=True)
    file_path = os.path.join(followed_users_folder, f"followed_users_{cl.user_id}.txt")

    with open(file_path, "a") as file:
        file.write(f"{user_id},{datetime.datetime.now()}\n")

def load_followed_users(cl: Client) -> List[Tuple[int, datetime.datetime]]:
    """Load followed users' IDs and timestamps from a file."""
    followed_users = []

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

def filter_users_to_unfollow(followed_users: List[Tuple[int, datetime.datetime]], follow_time: str) -> List[int]:
    """Filter users that should be unfollowed based on follow_time."""
    now = datetime.datetime.now()
    follow_time_seconds = utils.parse_time_string(follow_time)
    return [user for user, timestamp, *unfollow_timestamp in followed_users if (now - timestamp).total_seconds() >= follow_time_seconds and not unfollow_timestamp]


def remove_unfollowed_user(cl: Client, user: int) -> None:
    """Remove unfollowed user from the followed users file."""
    followed_users = load_followed_users(cl)
    followed_users.remove(user)

    os.makedirs(followed_users_folder, exist_ok=True)
    file_path = os.path.join(followed_users_folder, f"followed_users_{cl.user_id}.txt")

    with open(file_path, "w") as file:
        for user in followed_users:
            file.write(f"{user}\n")

def mark_unfollowed_user(cl: Client, user_id: int) -> None:
    """Mark the unfollowed user with a timestamp in the followed users file."""
    followed_users = load_followed_users(cl)
    followed_users = [(user, timestamp) if user != user_id else (user, timestamp, datetime.datetime.now()) for user, timestamp in followed_users]

    os.makedirs(followed_users_folder, exist_ok=True)
    file_path = os.path.join(followed_users_folder, f"followed_users_{cl.user_id}.txt")

    with open(file_path, "w") as file:
        for user_info in followed_users:
            file.write(",".join(str(x) for x in user_info) + "\n")

async def unfollow_users(cl: Client, account: Dict[str, Any]) -> None:
    """Unfollow users after a specified time."""
    utils.logger.info("Started unfollowing process")
    unfollow_after = account["unfollow_users"]["unfollow_after"]
    followed_users = load_followed_users(cl)
    users_to_unfollow = filter_users_to_unfollow(followed_users, follow_time=unfollow_after)
    unfollow_users_count = len(users_to_unfollow)
    utils.logger.info(f"Going to unfollow {unfollow_users_count} users")
    for user in users_to_unfollow:
        sleep_time = utils.calculate_sleep_time(unfollow_users_count)
        utils.logger.info(f"Sleeping for {sleep_time} before unfollowing {user}")
        await asyncio.sleep(sleep_time)
        try:
            cl.user_unfollow(user)
        except Exception as e:
            utils.logger.exception('Error while trying to unfollow user')
            continue

        utils.logger.info(f"Tried to unfollow user {user}")
        mark_unfollowed_user(cl, user)

def user_not_followed_before(cl: Client, user_id: int) -> bool:
    """Check if the given user_id has been followed before."""
    followed_users = load_followed_users(cl)
    for user, _ in followed_users:
        if user == user_id:
            return False
    return True

async def follow_user(cl: Client, user_id: int, engagement: Dict[str, Any]) -> bool:
    """Follow a user and add it to followed_users file."""

    if user_not_followed_before(cl, user_id):
        try:
            cl.user_follow(user_id)
            save_followed_user(cl, user_id=user_id)

        except:
            utils.logger.exception('Error while trying to follow user')
            return False

        if engagement["like_recent_posts"]:
            await like.like_recent_posts(cl, user_id=user_id, engagement=engagement)

        utils.logger.info(f"Followed user: {user_id}")

        return True

    utils.logger.info("User was followed before, skipped")

    return False


async def follow_user_followers(cl: Client, account: Dict[str, Any]) -> None:
    """Follow the followers of the source account and engage with their content."""
    utils.logger.info("Started following user followers process..")

    source_account = account['follow_users']['source_account']
    follows_per_day = account['follow_users']['follows_per_day']
    engagement = account['follow_users']['engagement']

    try:
        user_id = cl.user_id_from_username(source_account)
    except Exception as e:
        utils.logger.error(f"Error while trying to get user id from username {source_account}: {e}")
        return

    average_sleep_time = 86400 / follows_per_day
    min_sleep_time = average_sleep_time * 0.5
    max_sleep_time = average_sleep_time * 1.5

    try:
        users = cl.user_followers(user_id, True, amount=follows_per_day)
    except Exception as e:
        utils.logger.error(f"Error while trying to get followers of user {user_id}: {e}")
        return

    async def process_user(user):
        try:
            if await follow_user(cl, user, engagement):
                sleep_time = random.uniform(min_sleep_time, max_sleep_time)
                utils.logger.info(f"Sleeping for {sleep_time} seconds before following next user..")
                await asyncio.sleep(sleep_time)
        except Exception as e:
            utils.logger.error(f"Error while processing user {user}: {e}")

    async def sequential_follow():
        for user in users:
            await process_user(user)

    follow_task = asyncio.create_task(sequential_follow())
    await follow_task
