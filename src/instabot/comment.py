from instagrapi import Client
from typing import Dict, Any
import os
import datetime
import random
import asyncio
from instabot import utils
from instabot import media

async def comment_on_media(cl: Client, account: Dict[str, Any]):
    comment_on_tag = account['comment_on_media']['comment_on_tag']
    amount_per_day = account['comment_on_media']['amount_per_day']

    for i in range(1, amount_per_day):
        utils.logger.info(f"Commenting on post { i } / {amount_per_day}")

        post = media.recent_medias_hashtag_no_auth(comment_on_tag, 1)
        comment = random.choice(account['comment_on_media']['comments'])

        cl.media_comment(post[0].id, comment)

        sleep_time = utils.calculate_sleep_time(amount_per_day)
        await asyncio.sleep(sleep_time)

## You could save a comment and delete it after a certain amount of time.
## Deleting a comment not implemented yet.
def save_comment(comment_pk: int, username: str):
    comment_folder = "./artifacts/logs/comments"
    os.makedirs(comment_folder, exist_ok=True)
    comment_file_path = os.path.join(comment_folder, f"comments_{username}.json")

    with open(comment_file_path, "a") as file:
        file.write(f"{comment_pk},{datetime.datetime.now()}\n")
        utils.logger.info(f"Saved comment_pk to file for {username}")
