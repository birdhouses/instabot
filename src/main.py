from instabot import utils, follow, comment, upload, download, dm
import asyncio
from threading import Thread
from instagrapi import Client

async def main(account):
    username = account['account_details']['username']

    utils.logger.info(f'Started process for {username}')

    async with asyncio.TaskGroup() as tg:
        if account['follow_users']['enabled']:
            cl = await utils.get_client(account)
            follow_task = tg.create_task(
                follow.follow_user_followers(cl, account)
            )
        if account['unfollow_users']['enabled']:
            cl = await utils.get_client(account)
            unfollow_task = tg.create_task(
                follow.unfollow_users(cl, account)
            )
        if account['comment_on_media']['enabled']:
            cl = await utils.get_client(account)
            comment_task = tg.create_task(
                comment.comment_on_media(cl, account)
            )
        if account['upload_posts']['enabled']:
            cl = await utils.get_client(account)
            upload_task = tg.create_task(
                upload.upload_media(cl, account)
            )
        if account['upload_stories']['enabled']:
            cl = await utils.get_client(account)
            upload_task = tg.create_task(
                upload.upload_stories(cl, account)
            )

        if account['download_posts_from_account']['enabled']:
            cl = Client()
            download_task = tg.create_task(
                download.download_media(cl, account)
            )
        if account['dm_accounts_from_list']['enabled']:
            cl = await utils.get_client(account)
            dm_task = tg.create_task(
                dm.dm_from_list(cl, account)
            )

def run_account(account):
    asyncio.run(main(account))

if __name__ == "__main__":
    config = utils.load_config('./config.json')

    # Get the accounts from the configuration file
    accounts = config['accounts']

    # Create a thread for each account and run the main function
    account_threads = []
    for account in accounts:
        account_thread = Thread(target=run_account, args=(account,))
        account_threads.append(account_thread)
        account_thread.start()

    # Wait for all account threads to finish
    for account_thread in account_threads:
        account_thread.join()