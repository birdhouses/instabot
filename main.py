import instabot
import asyncio
from instabot import follow_user_followers, unfollow_users, comment_on_media

async def main(accounts):
    for account in accounts:
        username = account['username']
        password = account['password']

        cl = instabot.get_client(username, password)

        async with asyncio.TaskGroup() as tg:
            if account['follow_users']['enabled']:
                follow_task = tg.create_task(
                    follow_user_followers(cl, account)
                )
            if account['unfollow_users']['enabled']:
                unfollow_task = tg.create_task(
                    unfollow_users(cl, account['unfollow_users']['unfollow_after_days'])
                )
            if account['comment_on_media']['enabled']:
                comment_task = tg.create_task(
                    comment_on_media(cl, account)
                )

        print("All tasks have finished...")
if __name__ == "__main__":
    config = instabot.load_config('config.json')

    # Get the accounts from the configuration file
    accounts = config['accounts']
    asyncio.run(main(accounts))