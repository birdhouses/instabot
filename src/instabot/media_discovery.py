import instabot
import asyncio
import langdetect
from instagrapi import Client
import os

async def media_auto_discovery(account):
    config = account['media_auto_discovery']

    client = instabot.get_client(account['username'], account['password'])

    while True:
        posts = client.hashtag_medias_top(config['from_tag'])
        sleep_time = instabot.calculate_sleep_time(config['amount_per_day'])
        for post in posts:
            if await passes_requirements(client, post, config):
                store_post(client, account, post)
                asyncio.sleep(sleep_time)


async def passes_requirements(cl, post, config):
    post = cl.media_info(post.id)
    if post.like_count < config['post_requirements']['min_likes']:
        instabot.logger.info(f"Post {post.id} has less than {config['post_requirements']['min_likes']} likes")
        return False
    if post.comment_count < config['post_requirements']['min_comments']:
        instabot.logger.info(f"Post {post.id} has less than {config['post_requirements']['min_comments']} comments")
        return False
    if config['post_requirements']['detect_caption_language']:
        try:
            detected_language = langdetect.detect(post.caption_text)
            if detected_language not in config['post_requirements']['languages']:
                instabot.logger.info(f"Post {post.id} has language {detected_language} not in {config['post_requirements']['languages']}")
                return False
        except:
            instabot.logger.info(f"Post {post.id} caption has no language")
            return True
    if not post_type_check(post, config):
        instabot.logger.info(f"Post {post.id} has type {post.media_type} not in {config['post_requirements']['allowed_post_types']}")
        return False
    if config['author_requirements']['enabled']:
        author = cl.user_info_by_username(post.user.username)
        if config['author_requirements']['min_followers'] >= author.follower_count:
            instabot.logger.info(f"Author has less than {config['author_requirements']['min_followers']} followers")
            return False
        if config['author_requirements']['max_following'] <= author.following_count:
            instabot.logger.info(f"Author has more than {config['author_requirements']['max_following']} following")
            return False
        if config['author_requirements']['detect_biography_keywords']:
            if not has_keywords(author.biography, config['author_requirements']['biography_keywords']):
                instabot.logger.info(f"Author biography does not have keywords in {config['author_requirements']['biography_keywords']}")
            return False
        if config['author_requirements']['detect_biography_language']:
            try:
                detected_language = langdetect.detect(author.biography)
                if detected_language not in config['author_requirements']['languages']:
                    instabot.logger.info(f"Author biography has language {detected_language} not in {config['author_requirements']['languages']}")
                    return False
            except:
                instabot.logger.info(f"Author biography has no language")
                return True
    return True

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

def post_type_check(post, config):
    post_type = get_post_type(post)
    allowed_post_types = config['post_requirements']['allowed_post_types']
    allowed_post_types_lower = [post_type.lower() for post_type in allowed_post_types]
    if post_type != None:
        if allowed_post_types_lower is None:
            return True
        if post_type not in allowed_post_types_lower:
            instabot.logger.info(f"Post {post.id} has type {post.media_type} not in {config['post_requirements']['types']}")
            return False
        return True

def has_keywords(biography, keywords):
    biography_lower = biography.lower()
    return any(keyword.lower() in biography_lower for keyword in keywords)

def store_post(cl, account, post):
    photo_download_path = f"./saved_posts/{account['username']}/photo_downloads"
    video_download_path = f"./saved_posts/{account['username']}/video_downloads"
    album_download_path = f"./saved_posts/{account['username']}/album_downloads"
    if post.media_type == 1:
        os.makedirs(photo_download_path, exist_ok=True)
        try:
            cl.photo_download(post.pk, photo_download_path)
        except:
            instabot.logger.info(f"Failed to download photo for post {post.id}")
    elif post.media_type == 2:
        os.makedirs(video_download_path, exist_ok=True)
        try:
            cl.video_download(post.pk, video_download_path)
        except:
            instabot.logger.info(f"Failed to download video for post {post.id}")
    elif post.media_type == 8:
        os.makedirs(album_download_path, exist_ok=True)
        try:
            cl.album_download(post.pk, album_download_path)
        except:
            instabot.logger.info(f"Failed to download album for post {post.id}")
