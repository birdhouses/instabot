from instagrapi import Client
import logging
import time
from typing import List, Dict, Any
import os
import datetime
import random
from instabot import calculate_sleep_time

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/bot.log")
    ]
)

logger = logging.getLogger()

def comment_on_media(cl: Client, account: Dict[str, Any]) -> None:
    comment_on_tag = account['comment_on_media']['comment_on_tag']
    amount_per_day = account['comment_on_media']['amount_per_day']

    posts_to_comment = cl.hashtag_medias_recent(comment_on_tag, amount_per_day)

    for post in posts_to_comment:
        comment = random.choice(account['comment_on_media']['comments'])

        sleep_time = calculate_sleep_time(amount_per_day)
        logger.info(f"Sleeping for {sleep_time} before commenting")
        time.sleep(sleep_time)
        cl.media_comment(post.id, comment)

        logger.info(f"Commented on post {post.id}")