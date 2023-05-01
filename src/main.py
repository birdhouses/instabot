from instabot import utils, follow, comment, media
import asyncio
from threading import Thread
from instagrapi import Client

async def main(account):
    username = account['username']
    password = account['password']

    utils.logger.info(f'Started process for {username}')

    while True:
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
            if account['media_auto_discovery']['enabled']:
                # anon_cl = Client(request_timeout=account['media_auto_discovery']['request_timeout'])
                cl = await utils.get_client(account)
                media_task = tg.create_task(
                    media.media_auto_discovery(cl, account)
                )

def run_account(account):
    asyncio.run(main(account))

if __name__ == "__main__":
    config = utils.load_config('../config.json')

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