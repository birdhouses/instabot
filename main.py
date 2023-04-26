import instabot
import asyncio
from instabot import follow_user_followers, unfollow_users, comment_on_media
from instabot import logger
from threading import Thread

async def main(account):
    username = account['username']
    password = account['password']

    logger.info(f'Started process for {username}')

    async with asyncio.TaskGroup() as tg:
        if account['follow_users']['enabled']:
            cl = instabot.get_client(username, password)
            follow_task = tg.create_task(
                follow_user_followers(cl, account)
            )
        if account['unfollow_users']['enabled']:
            cl = instabot.get_client(username, password)
            unfollow_task = tg.create_task(
                unfollow_users(cl, account['unfollow_users']['unfollow_after_days'])
            )
        if account['comment_on_media']['enabled']:
            cl = instabot.get_client(username, password)
            comment_task = tg.create_task(
                comment_on_media(cl, account)
            )

def run_account(account):
    asyncio.run(main(account))

if __name__ == "__main__":
    config = instabot.load_config('config.json')

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