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
    captions_file = account['upload_posts'].get('captions_file')  # Captions file path
    posts_dir = account['upload_posts']['posts_dir']
    delete_after_upload = account['upload_posts']['delete_after_upload']
    post_folders = get_post_folders(posts_dir)

    random.shuffle(post_folders)
    captions = load_captions(captions_file)

    for folder in post_folders:
        sleep_time = utils.calculate_sleep_time(amount)
        TimeKeeper(username, 'upload_media', sleep_time)
        await asyncio.sleep(sleep_time)

        folder_path = os.path.join(posts_dir, folder)
        caption = get_caption_from_folder(folder_path) or random.choice(list(captions.values()))  # Get caption or random

        if is_album(folder_path):
            upload_album(cl, folder_path, caption, delete_after_upload)
        elif is_video_in_folder(folder_path):
            upload_video(cl, folder_path, caption, delete_after_upload)
        elif is_image_post(folder_path):
            upload_post(cl, folder_path, caption, delete_after_upload)
        else:
            utils.logger.warning(f"{folder} is not a valid post or album.")

def is_image_file(file_path: str) -> bool:
    """Checks if a file is an image."""
    return file_path.lower().endswith(('.jpg', '.jpeg', '.png'))

def is_video(media: str) -> bool:
    """Checks if a file is a video."""
    return media.lower().endswith('.mp4')

def is_image_post(folder_path: str) -> bool:
    """Checks if a folder contains a single image post."""
    return any(is_image_file(file) for file in os.listdir(folder_path))

def is_video_in_folder(folder_path: str) -> bool:
    """Checks if a folder contains a video file."""
    return any(is_video(file) for file in os.listdir(folder_path))

def upload_album(cl, folder_path, caption, delete_after_upload):
    """Uploads an album to Instagram."""
    posts = get_posts(folder_path)
    new_paths = []

    for image_path in posts:
        full_path = os.path.join(folder_path, image_path)
        ext = os.path.splitext(image_path)[1].lower()
        output_path = full_path

        if ext in [".jpg", ".jpeg"]:
            new_paths.append(full_path)
        elif ext == ".png":
            # Convert PNG to JPG using utility function
            output_path = full_path.replace(".png", ".jpg")
            try:
                utils.convert_png_to_jpg(full_path, output_path)
                new_paths.append(output_path)
            except Exception as e:
                utils.logger.error(f"Error converting PNG to JPG for {full_path}: {e}")
                continue
        elif ext == ".webp":
            # Convert WEBP to JPG using utility function
            output_path = full_path.replace(".webp", ".jpg")
            try:
                utils.convert_webp_to_jpg(full_path, output_path)
                new_paths.append(output_path)
            except Exception as e:
                utils.logger.error(f"Error converting WEBP to JPG for {full_path}: {e}")
                continue
        elif ext == ".mp4":
            new_paths.append(full_path)
        else:
            utils.logger.warning(f"Unsupported file format {ext} in {full_path}, skipping.")

    if new_paths:
        try:
            cl.album_upload(new_paths, caption)
            if delete_after_upload:
                shutil.rmtree(folder_path)
            utils.logger.info(f"Uploaded album from {folder_path}")
        except instabot.exceptions.AlbumUnknownFormat as e:
            utils.logger.error(f"Error uploading album {folder_path}: Unknown format. {e}")
        except Exception as e:
            utils.logger.error(f"Error uploading album {folder_path}: {e}")
    else:
        utils.logger.warning(f"No valid media found in album {folder_path}")

def is_album(folder_path: str) -> bool:
    """Determines if a folder contains an album (more than one media file)."""
    valid_media = ['.jpg', '.jpeg', '.png', '.mp4', '.webp']
    media_files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in valid_media]
    return len(media_files) > 1

def upload_album(cl, folder_path, caption, delete_after_upload):
    """Uploads an album to Instagram."""
    posts = get_posts(folder_path)
    new_paths = []

    for image_path in posts:
        full_path = os.path.join(folder_path, image_path)
        ext = os.path.splitext(image_path)[1].lower()
        output_path = full_path

        if ext in [".jpg", ".jpeg"]:
            new_paths.append(full_path)
        elif ext == ".png":
            # Convert PNG to JPG
            output_path = full_path.replace(".png", ".jpg")
            try:
                with Image.open(full_path) as img:
                    rgb_img = img.convert('RGB')
                    rgb_img.save(output_path)
                new_paths.append(output_path)
            except Exception as e:
                utils.logger.error(f"Error converting PNG to JPG for {full_path}: {e}")
                continue
        elif ext == ".webp":
            # Convert WEBP to JPG
            output_path = full_path.replace(".webp", ".jpg")
            try:
                utils.convert_webp_to_jpg(full_path, output_path)
                new_paths.append(output_path)
            except Exception as e:
                utils.logger.error(f"Error converting WEBP to JPG for {full_path}: {e}")
                continue
        elif ext == ".mp4":
            new_paths.append(full_path)
        else:
            utils.logger.warning(f"Unsupported file format {ext} in {full_path}, skipping.")

    if new_paths:
        try:
            cl.album_upload(new_paths, caption)
            if delete_after_upload:
                shutil.rmtree(folder_path)
            utils.logger.info(f"Uploaded album from {folder_path}")
        except instabot.exceptions.AlbumUnknownFormat as e:
            utils.logger.error(f"Error uploading album {folder_path}: Unknown format. {e}")
        except Exception as e:
            utils.logger.error(f"Error uploading album {folder_path}: {e}")
    else:
        utils.logger.warning(f"No valid media found in album {folder_path}")

def upload_post(cl, folder_path, caption, delete_after_upload):
    """Uploads a single image post to Instagram."""
    image_files = [f for f in os.listdir(folder_path) if is_image_file(os.path.join(folder_path, f))]
    if not image_files:
        utils.logger.warning(f"No image found in {folder_path}")
        return
    image_path = os.path.join(folder_path, image_files[0])
    try:
        cl.photo_upload(image_path, caption)
    except Exception as e:
        utils.logger.error(f"Error uploading post {image_path}: {e}")
        return
    if delete_after_upload:
        shutil.rmtree(folder_path)
    utils.logger.info(f"Uploaded image post from {folder_path}")

def get_posts(directory: str) -> List[str]:
    """Retrieves a list of valid media files in a directory."""
    valid_images = [".jpg", ".jpeg", ".png", ".webp", ".mp4"]
    posts = []
    for filename in os.listdir(directory):
        ext = os.path.splitext(filename)[1].lower()
        if ext in valid_images:
            posts.append(filename)
        else:
            utils.logger.warning(f"Ignoring file with unexpected extension: {filename}")
    return posts

def get_post_folders(posts_dir: str) -> List[str]:
    """Retrieves a list of folders in the given directory."""
    return [f for f in os.listdir(posts_dir) if os.path.isdir(os.path.join(posts_dir, f))]

def get_caption_from_folder(folder_path: str) -> str:
    """Retrieves the caption from a caption.txt file in the given folder."""
    caption_file = os.path.join(folder_path, 'caption.txt')
    if not os.path.exists(caption_file):
        return ""
    try:
        with open(caption_file, 'r', encoding='utf-8') as f:
            caption = f.read().strip()
        return caption
    except Exception as e:
        utils.logger.error(f"Error reading caption file in {folder_path}: {e}")
        return ""

def load_captions(captions_file: str) -> dict:
    """Loads fallback captions from a file."""
    captions = {}
    if not captions_file:
        return captions

    try:
        with open(captions_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    media, caption = parts
                    captions[media] = caption
    except FileNotFoundError:
        utils.logger.warning(f"Captions file {captions_file} not found.")
    except Exception as e:
        utils.logger.error(f"Error reading captions file {captions_file}: {e}")

    return captions
