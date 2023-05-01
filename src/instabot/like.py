from instagrapi import Client
from instagrapi import utils
from typing import List, Dict, Any
import asyncio

async def like_recent_posts(cl: Client, user_id: int, engagement: Dict[str, Any]) -> None:
    like_count = engagement['like_count']
    recent_posts = cl.user_medias(user_id, amount=like_count)

    for post in recent_posts:
        try:
            sleep_time = utils.calculate_sleep_time(like_count)
            utils.logger.info(f"Sleeping for {sleep_time} seconds before liking")

            await asyncio.sleep(sleep_time)
            cl.media_like(post.id)

            utils.logger.info(f"Liked post {post.id} of user {user_id}")
        except Exception as e:
            utils.logger.error(f"Error liking post {post.id} of user {user_id}: {e}")