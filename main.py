import instabot
import threading

if __name__ == "__main__":
    config = instabot.load_config('config.json')

    ACCOUNT_USERNAME = config['account']['username']
    ACCOUNT_PASSWORD = config['account']['password']
    SOURCE_ACCOUNT = config['source_account']
    FOLLOWS_PER_DAY = config['follows_per_day']

    cl = instabot.get_client(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

    while True:
        follow_thread = threading.Thread(target=instabot.follow_users, args=(cl, SOURCE_ACCOUNT, FOLLOWS_PER_DAY))
        unfollow_thread = threading.Thread(target=instabot.unfollow_users, args=(cl, config))

        follow_thread.start()
        unfollow_thread.start()

        follow_thread.join()
        unfollow_thread.join()
