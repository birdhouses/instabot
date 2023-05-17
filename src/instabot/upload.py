import instabot
import asyncio
import os
from typing import Union, List
from instabot import utils

async def upload_media(cl, account):
    utils.logger.info("Uploading media...")

    posts = load_posts(account)
    amount = account['upload_posts']['amount_per_day']
    caption = account['upload_posts']['caption']
    posts_dir = account['upload_posts']['posts_dir']

    if len(posts) == 0:
        utils.logger.error("No posts found! Add some posts to the " + account['upload_posts']['posts_dir'] + " directory!")
        return
    elif len(posts) < amount:
        utils.logger.error(f"Found {len(posts)} posts, but {amount} per day configured! Add some posts to the " + account['upload_posts']['posts_dir'] + " directory")
        return
    else:
        utils.logger.info(f"Found {len(posts)} posts!")


    for path in posts:
        path_to_post = posts_dir + '/' + path

        if os.path.isfile(path_to_post):
            cl.photo_upload(path_to_post, caption)
            sleep_time = utils.calculate_sleep_time(amount)
            utils.logger.info(f"Sleeping for {sleep_time} seconds before uploading media...")

            await asyncio.sleep(sleep_time)
        else:
            utils.logger.error(f"File {path_to_post} does not exist!")
            return

def load_posts(account: dict) -> List[dict]:
    post_dir = account['upload_posts']['posts_dir']
    if not os.path.isdir(post_dir):
        utils.logger.error(f"Directory {post_dir} does not exist! Creating new directory...")
        os.mkdir(post_dir)

    posts = os.listdir(post_dir)

    if len(posts) == 0:
        return []

    return filter_posts(posts)

def filter_posts(posts):
    ## TODO:
    ## implement more post type filtering here
    valid_images = [".jpg", ".webp", ".png"]
    valid_posts = []
    for post in posts:
        ext = os.path.splitext(post)[1]
        if ext.lower() not in valid_images:
            continue
        valid_posts.append(post)

    return valid_posts