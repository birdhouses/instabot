import instabot
import asyncio
import os
from typing import Union, List
from instabot import utils
import random
import shutil
from humanfriendly import format_timespan
from instabot.timekeeper import TimeKeeper

async def upload_media(cl, account):
    utils.logger.info("Uploading media...")

    username = account['account_details']['username']
    amount = account['upload_posts']['amount_per_day']
    captions = account['upload_posts']['caption']
    posts_dir = account['upload_posts']['posts_dir']
    delete_after_upload = account['upload_posts']['delete_after_upload']
    medias = os.listdir(posts_dir)

    for media in medias:
        sleep_time = utils.calculate_sleep_time(amount)

        TimeKeeper(username, 'upload_media', sleep_time)

        await asyncio.sleep(sleep_time)

        caption = random.choice(captions)
        if is_post(media):
            upload_post(cl, media, posts_dir, caption, delete_after_upload)
        elif is_album(posts_dir, media):
            upload_album(cl, media, posts_dir, caption, delete_after_upload)
        elif is_video(media):
            upload_video(cl, media, posts_dir, caption, delete_after_upload)
        else:
            utils.logger.warning(f"{media} is not a valid post or album.")
            continue

def is_video(media: str) -> bool:
    return media.endswith('.mp4')

def upload_video(cl, path, posts_dir, caption, delete_after_upload):
    path_to_post = posts_dir + '/' + path

    try:
        cl.video_upload(path_to_post, caption)
    except Exception as e:
        utils.logger.error(f"Error uploading {path}: {e}")
        return

    if delete_after_upload:
        os.remove(path_to_post)

    utils.logger.info(f"Uploaded {path}")

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

    new_paths = []  # This will hold the paths for the converted images

    for image_path in paths:
        if is_post(image_path):
            output_path = image_path.replace(".webp", ".jpg")  # replace .webp with .jpg in the file path
            utils.convert_webp_to_jpg(image_path, output_path)
            new_paths.append(output_path)  # Append the new path to new_paths
        elif is_video(image_path):
            new_paths.append(image_path)  # Append the new path to new_paths

    cl.album_upload(new_paths, caption)  # Use new_paths here instead of paths

    if delete_after_upload:
        shutil.rmtree(path_to_album)  # Delete the entire album folder

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

    posts = sorted(posts, key=lambda filename: int(filename.split('_')[0]))

    return filter_posts(posts)

def get_albums(post_dir: str) -> List[str]:
    albums = []
    for file in os.listdir(post_dir):
        if os.path.isdir(post_dir + '/' + file):
            albums.append(file)
    return albums

def filter_posts(posts):
    valid_images = [".jpg", ".webp", ".png", ".mp4"]
    valid_posts = []
    for post in posts:
        ext = os.path.splitext(post)[1]
        if ext.lower() not in valid_images:
            continue
        valid_posts.append(post)

    return valid_posts