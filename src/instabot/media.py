import instabot
import asyncio
import langdetect
from instagrapi import Client
import os
from instabot import utils
from threading import Thread

MIN_LIKES = "min_likes"
MIN_COMMENTS = "min_comments"
DETECT_CAPTION_LANGUAGE = "detect_caption_language"
LANGUAGES = "languages"
ALLOWED_POST_TYPES = "allowed_post_types"

async def media_auto_discovery(client, account):
    config = account['media_auto_discovery']

    while True:
        try:
            posts = client.hashtag_medias_top(config['from_tag'], account['media_auto_discovery']['amount_per_day'])
            utils.logger.info(f"Auto-discovered {len(posts)} media posts")
        except Exception as e:
            utils.logger.error(f"Failed to auto-discover media posts: {e}")
            return await asyncio.sleep(1)

        for post in posts:
            utils.logger.info(f"Auto-discovered media {post.id}")
            if await passes_requirements(client, post, config):
                store_post(client, account, post)

        sleep_time = utils.get_approximate_sleep_time(hours=3)
        utils.logger.info(f"Sleeping for {sleep_time}")

        await asyncio.sleep(sleep_time)

async def passes_requirements(cl, post, config):
    return (await check_post_requirements(cl, post, config) and
            await check_author_requirements(cl, post, config))

async def check_post_requirements(cl, post, config):
    post_req = config['post_requirements']
    try:
        # post = cl.media_info(post.id)
        if post.like_count < post_req[MIN_LIKES] or post.comment_count < post_req[MIN_COMMENTS]:
            return False

        if post_req[DETECT_CAPTION_LANGUAGE]:
            if not is_language_allowed(post.caption_text, post_req[LANGUAGES]):
                return False

        if not is_post_type_allowed(post, post_req[ALLOWED_POST_TYPES]):
            return False

        return True

    except Exception as e:
        utils.logger.error(f"Failed to check post requirements: {e}")

async def check_author_requirements(cl, post, config):
    author_req = config['author_requirements']
    if not author_req['enabled']:
        return True

    author = cl.user_info_by_username(post.user.username)

    if (author_req['min_followers'] >= author.follower_count or
            author_req['max_following'] <= author.following_count):
        return False

    if author_req['detect_biography_keywords']:
        if not has_keywords(author.biography, author_req['biography_keywords']):
            return False

    if author_req['detect_biography_language']:
        if not is_language_allowed(author.biography, author_req[LANGUAGES]):
            return False

    return True

def is_language_allowed(text, allowed_languages):
    try:
        detected_language = langdetect.detect(text)
        return detected_language in allowed_languages
    except:
        return True

def is_post_type_allowed(post, allowed_post_types):
    post_type = get_post_type(post)
    return post_type is None or post_type.lower() in allowed_post_types

def get_post_type(post):
    if post.media_type == 1:
        return 'photo'
    elif post.media_type == 2 and post.product_type == 'feed':
        return 'video'
    elif post.media_type == 2 and post.product_type == 'igtv':
        return 'igtv'
    elif post.media_type == 8:
        return 'album'
    return None

def has_keywords(biography, keywords):
    biography_lower = biography.lower()
    return any(keyword.lower() in biography_lower for keyword in keywords)

def store_post(cl, account, post):
    photo_download_path = f"./saved_posts/{account['username']}/photo_downloads/post_{post.pk}"
    video_download_path = f"./saved_posts/{account['username']}/video_downloads/post_{post.pk}"
    album_download_path = f"./saved_posts/{account['username']}/album_downloads/post_{post.pk}"

    if post.media_type == 1:
        saved_path = download_photo(cl, post, photo_download_path)
        save_caption_for_single(post.caption_text, saved_path)
    elif post.media_type == 2:
        saved_path = download_video(cl, post, video_download_path)
        save_caption_for_single(post.caption_text, saved_path)
    elif post.media_type == 8:
        saved_path = download_album(cl, post, album_download_path)
        save_caption_for_album(post.caption_text, saved_path)

def download_photo(cl, post, photo_download_path):
    os.makedirs(photo_download_path, exist_ok=True)
    try:
        return cl.photo_download(post.pk, photo_download_path)
    except:
        utils.logger.info(f"Failed to download photo for post {post.id}")
        return False

def download_video(cl, post, video_download_path):
    os.makedirs(video_download_path, exist_ok=True)
    try:
        return cl.video_download(post.pk, video_download_path)
    except:
        utils.logger.info(f"Failed to download video for post {post.id}")
        return False

def download_album(cl, post, album_download_path):
    os.makedirs(album_download_path, exist_ok=True)
    try:
        return cl.album_download(post.pk, album_download_path)
    except:
        utils.logger.info(f"Failed to download album for post {post.id}")
        return False

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

def save_caption_for_single(caption, path):
    # Remove the file extension and add '.txt'
    txt_path = os.path.splitext(path)[0] + '.txt'
    utils.logger.info(f"Saving caption to {txt_path}")

    try:
        with open(txt_path, 'w') as f:
            f.write(caption)
    except Exception as e:
        utils.logger.info(f"Failed to save caption to {txt_path}. {e}")
        return False

def save_caption_for_album(caption, paths):
    for path in paths:
        # Remove the file extension and add '.txt'
        txt_path = os.path.splitext(path)[0] + '.txt'
        utils.logger.info(f"Saving caption to {txt_path}")

        try:
            with open(txt_path, 'w') as f:
                f.write(caption)
                return True

        except Exception as e:
            utils.logger.info(f"Failed to save caption to {txt_path}. {e}")
            return False

    return True