from instagrapi import Client
import logging
import time
from typing import List, Dict, Any
import os
import datetime
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

def like_recent_posts(cl: Client, user_id: int, engagement: Dict[str, Any]) -> None:
    like_count = engagement['like_count']
    min_sleep = 30
    max_sleep = 180
    recent_posts = cl.user_medias(user_id, amount=like_count)

    for post in recent_posts:
        sleep_time = random.uniform(min_sleep, max_sleep)
        time.sleep(sleep_time)
        cl.media_like(post.id)
        logger.info(f"Liked post {post.id} of user {user_id}")