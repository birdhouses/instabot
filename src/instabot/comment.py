from instagrapi import Client
from typing import Dict, Any
import os
import datetime
import random
import asyncio
from instabot import utils
from instabot import media

async def comment_on_media(cl: Client, account: Dict[str, Any]):
    try:
        comment_on_tag = account['comment_on_media']['comment_on_tag']
        amount_per_day = account['comment_on_media']['amount_per_day']

        posts_to_comment = media.recent_medias_hashtag_no_auth(comment_on_tag, amount_per_day)

        if posts_to_comment:
            for post in posts_to_comment:
                try:
                    comment = random.choice(account['comment_on_media']['comments'])

                    sleep_time = utils.calculate_sleep_time(amount_per_day)
                    utils.logger.info(f"Sleeping for {sleep_time} before commenting")
                    await asyncio.sleep(sleep_time)

                    comment = cl.media_comment(post.id, comment)

                    save_comment(comment.pk, account['username'])

                    utils.logger.info(f"Commented on post {post.id}")
                except Exception as e:
                    utils.logger.error(f"Error while commenting on media {post['pk']}: {e}")
                    # Continue with the next iteration without stopping the whole task
                continue
        else:
            utils.logger.info(f"No posts to comment on")
            return await asyncio.sleep(0)

    except Exception as e:
        utils.logger.error(f"Error while fetching media for hashtag {comment_on_tag}: {e}")
         # Exit the current task without affecting other tasks
        return await asyncio.sleep(0)


def save_comment(comment_pk: int, username: str):
    comment_folder = "./artifacts/logs/comments"
    os.makedirs(comment_folder, exist_ok=True)
    comment_file_path = os.path.join(comment_folder, f"comments_{username}.json")

    with open(comment_file_path, "a") as file:
        file.write(f"{comment_pk},{datetime.datetime.now()}\n")
        utils.logger.info(f"Saved comment_pk to file for {username}")
