from instagrapi import Client
from typing import List, Dict, Any
import random
import asyncio
from instabot import logger

async def like_recent_posts(cl: Client, user_id: int, engagement: Dict[str, Any]) -> None:
    like_count = engagement['like_count']
    min_sleep = 30
    max_sleep = 180
    recent_posts = cl.user_medias(user_id, amount=like_count)

    for post in recent_posts:
        sleep_time = random.uniform(min_sleep, max_sleep)
        await asyncio.sleep(sleep_time)
        cl.media_like(post.id)
        logger.info(f"Liked post {post.id} of user {user_id}")