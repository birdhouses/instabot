import instabot
import asyncio
import os
from typing import Union, List
from instabot import utils

async def upload_media(cl, account):
    utils.logger.info("Uploading media...")

    amount = account['upload_posts']['amount_per_day']
    caption = account['upload_posts']['caption']
    posts_dir = account['upload_posts']['posts_dir']
    delete_after_upload = account['upload_posts']['delete_after_upload']
    medias = os.listdir(posts_dir)

    for media in medias:
        if is_post(media):
            upload_post(cl, media, posts_dir, caption, delete_after_upload)
        elif is_album(posts_dir, media):
            upload_album(cl, media, posts_dir, caption, delete_after_upload)
        else:
            utils.logger.warning(f"{media} is not a valid post or album.")
            continue

        sleep_time = utils.calculate_sleep_time(amount)
        await asyncio.sleep(sleep_time)

def is_album(posts_dir: str, path: str) -> bool:
    if not os.path.isdir(posts_dir + '/' + path):
        return False

    posts = get_posts(posts_dir + '/' + path)

    return len(posts) > 0

def is_post(path: str) -> bool:
    valid_images = [".jpg", ".webp", ".png"]
    ext = os.path.splitext(path)[1]
    if ext.lower() not in valid_images:

        return False

    return True

def upload_album(cl, album: str, posts_dir, caption: str, delete_after_upload: bool):
    path_to_album = posts_dir + '/' + album
    posts = get_posts(path_to_album)

    paths = []
    for path in posts:
        paths.append(path_to_album + '/' + path)

    cl.album_upload(paths, caption)

    if delete_after_upload:
        os.remove(path_to_album)

    utils.logger.info(f"Uploaded {album}")

def upload_post(cl, path, posts_dir, caption, delete_after_upload):
        path_to_post = posts_dir + '/' + path

        cl.photo_upload(path_to_post, caption)

        if delete_after_upload:
            os.remove(path_to_post)

        utils.logger.info(f"Uploaded {path}")

def get_posts(post_dir: str) -> List[str]:
    posts = []
    for file in os.listdir(post_dir):
        if os.path.isfile(post_dir + '/' + file):
            posts.append(file)
    return filter_posts(posts)

def get_albums(post_dir: str) -> List[str]:
    albums = []
    for file in os.listdir(post_dir):
        if os.path.isdir(post_dir + '/' + file):
            albums.append(file)
    return albums

def filter_posts(posts):
    valid_images = [".jpg", ".webp", ".png"]
    valid_posts = []
    for post in posts:
        ext = os.path.splitext(post)[1]
        if ext.lower() not in valid_images:
            continue
        valid_posts.append(post)

    return valid_posts