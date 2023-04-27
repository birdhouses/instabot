import instabot
import asyncio
import langdetect
from instagrapi import Client

async def media_auto_discovery(account):
    config = account['media_auto_discovery']
    get_posts_cl = Client()
    posts = get_posts_cl.hashtag_medias_top(config['from_tag'])

    for post in posts:
        reqs_check_client = Client()
        if passes_requirements(reqs_check_client, post, config):
            save_post(account, post)

async def passes_requirements(cl, post, config):
    post = await cl.media_info(post.id)
    if post.like_count < config['post_requirements']['min_likes']:
        instabot.logger.info(f"Post {post.id} has less than {config['post_requirements']['min_likes']} likes")
        return False
    if post.comment_count < config['post_requirements']['min_comments']:
        instabot.logger.info(f"Post {post.id} has less than {config['post_requirements']['min_comments']} comments")
        return False
    if config['post_requirements']['detect_caption_language']:
        detected_language = langdetect.detect(post.caption_text)
        if detected_language not in config['post_requirements']['languages']:
            instabot.logger.info(f"Post {post.id} has language {detected_language} not in {config['post_requirements']['languages']}")
            return False
    if config['author_requirements']['enabled']:
        author = await cl.user_info_by_username(post.user.username)
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
            detected_language = langdetect.detect(author.biography)
            if detected_language not in config['author_requirements']['languages']:
                instabot.logger.info(f"Author biography has language {detected_language} not in {config['author_requirements']['languages']}")
                return False
    return True

def has_keywords(biography, keywords):
    biography_lower = biography.lower()
    return any(keyword.lower() in biography_lower for keyword in keywords)

def save_post(account, post):
    print("To be implemented")