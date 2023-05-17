import instabot
import os
import asyncio

async def download_media(cl, account):
    instabot.utils.logger.info("Downloading media...")
    source_account = account['download_posts_from_account']['source_account']
    amount = account['download_posts_from_account']['amount']
    timeout = account['download_posts_from_account']['timeout']

    id = cl.user_id_from_username(source_account)
    posts = cl.user_medias_gql(id, amount, timeout)

    for post in posts:
        post_download_path = f"./saved_posts/{account['username']}/from_account/{source_account}"
        os.makedirs(post_download_path, exist_ok=True)
        cl.photo_download(post.pk, post_download_path)
        instabot.utils.logger.info(f"Downloaded {post.pk} to {post_download_path}")