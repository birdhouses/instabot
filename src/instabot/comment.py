from instagrapi import Client
import logging
import time
from typing import List, Dict, Any
import os
import datetime
import random
from instabot import calculate_sleep_time, logger
import asyncio

async def comment_on_media(cl: Client, account: Dict[str, Any]) -> None:
    try:
        comment_on_tag = account['comment_on_media']['comment_on_tag']
        amount_per_day = account['comment_on_media']['amount_per_day']

        posts_to_comment = cl.hashtag_medias_recent(comment_on_tag, amount_per_day)

        for post in posts_to_comment:
            try:
                comment = random.choice(account['comment_on_media']['comments'])

                sleep_time = calculate_sleep_time(amount_per_day)
                logger.info(f"Sleeping for {sleep_time} before commenting")
                await asyncio.sleep(sleep_time)

                comment = cl.media_comment(post.id, comment)

                save_comment(comment.pk, account['username'])

                logger.info(f"Commented on post {post.id}")
            except Exception as e:
                logger.error(f"Error while commenting on media {post['pk']}: {e}")
                # Continue with the next iteration without stopping the whole task
            continue

    except Exception as e:
        logger.error(f"Error while fetching media for hashtag {comment_on_tag}: {e}")
         # Exit the current task without affecting other tasks
        return

def save_comment(comment_pk: int, username: str):
    comment_folder = "./artifacts/logs/comments"
    os.makedirs(comment_folder, exist_ok=True)
    comment_file_path = os.path.join(comment_folder, f"comments_{username}.json")

    with open(comment_file_path, "a") as file:
        file.write(f"{comment_pk},{datetime.datetime.now()}\n")
        logger.info(f"Saved comment_pk to file for {username}")
