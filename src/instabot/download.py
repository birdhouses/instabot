import instabot
import os
import asyncio

async def download_media(cl, account):
    instabot.utils.logger.info("Downloading media...")
    source_account = account['download_posts_from_account']['source_account']
    amount = account['download_posts_from_account']['amount']
    timeout = account['download_posts_from_account']['timeout']
    save_path = account['download_posts_from_account']['save_path']

    if amount == '':
        # Default amount is 20
        amount = 20
    if timeout == '':
        # Default timeout is 2 seconds
        timeout = 2

    id = cl.user_id_from_username(source_account)
    posts = cl.user_medias_gql(id, amount, timeout)

    for post in posts:
        post_download_path = f"{save_path}"
        os.makedirs(post_download_path, exist_ok=True)
        media_info = cl.media_info(post.pk).dict()

        if media_info['media_type']  == 1:
            cl.photo_download(post.pk, post_download_path)
        elif media_info['media_type'] == 2 and media_info['product_type'] == 'feed':
            cl.video_download(post.pk, post_download_path)
        elif media_info['media_type'] == 2 and media_info['product_type'] == 'igtv':
            cl.igtv_download(post.pk, post_download_path)
        elif media_info['media_type'] == 2 and media_info['product_type'] == 'clips':
            cl.clip_download(post.pk, post_download_path)
        elif media_info['media_type'] == 8:
            album_path = f"{post_download_path}/{post.pk}"
            os.makedirs(album_path, exist_ok=True)
            result = cl.album_download(post.pk, album_path)
            for i, path in enumerate(result):
                new_path = path.parent / f"{i}_{path.name}"  # Add the index number to the filename
                path.rename(new_path)  # Rename the file

    instabot.utils.logger.info(f"Downloaded {amount} posts from {source_account}")