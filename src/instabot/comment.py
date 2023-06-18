from instagrapi import Client
from typing import Dict, Any
import os
import datetime
import random
import asyncio
from instabot import utils

async def comment_on_media(cl: Client, account: Dict[str, Any]):
    comment_on_tag = account['comment_on_media']['comment_on_tag']
    amount_per_day = account['comment_on_media']['amount_per_day']

    for i in range(1, amount_per_day):
        utils.logger.info(f"Commenting on post { i } / {amount_per_day}")

        post = recent_medias_hashtag_no_auth(comment_on_tag, 1)
        comment = random.choice(account['comment_on_media']['comments'])

        cl.media_comment(post[0].id, comment)

        sleep_time = utils.calculate_sleep_time(amount_per_day)
        await asyncio.sleep(sleep_time)

def recent_medias_hashtag_no_auth(tag: str, amount: int):
    client = Client()
    try:
        try:
            posts = client.hashtag_medias_recent_a1(tag, amount)
        except:
            posts = client.hashtag_medias_recent_v1(tag, amount)

        return posts
    except Exception as e:
        utils.logger.info(f"Failed to get recent medias for tag {tag}. {e}")
        return False
