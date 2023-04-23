import instabot
import threading

def run_bot(account):
    username = account['username']
    password = account['password']
    source_account = account['source_account']
    follows_per_day = account['follows_per_day']
    unfollow_after = account['unfollow_after']

    cl = instabot.get_client(username, password)

    while True:
        follow_thread = threading.Thread(target=instabot.follow_users, args=(cl, source_account, follows_per_day))
        unfollow_thread = threading.Thread(target=instabot.unfollow_users, args=(cl, unfollow_after))

        follow_thread.start()
        unfollow_thread.start()

        follow_thread.join()
        unfollow_thread.join()

if __name__ == "__main__":
    config = instabot.load_config('config.json')

    # Get the accounts from the configuration file
    accounts = config['accounts']

    # Create a thread for each account and run the bot
    account_threads = []
    for account in accounts:
        account_thread = threading.Thread(target=run_bot, args=([account]))
        account_threads.append(account_thread)
        account_thread.start()

    # Wait for all account threads to finish
    for account_thread in account_threads:
        account_thread.join()
