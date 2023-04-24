import instabot
import threading

def run_bot(account):
    username = account['username']
    password = account['password']

    cl = instabot.get_client(username, password)
    worker_threads = []

    if account['follow_users']['enabled']:
        follow_thread = threading.Thread(target=instabot.follow_user_followers, args=(cl, account))
        worker_threads.append(follow_thread)
        follow_thread.start()
    if account['unfollow_users']['enabled']:
        unfollow_after = account['unfollow_users']['unfollow_after']
        unfollow_thread = threading.Thread(target=instabot.unfollow_users, args=(cl, unfollow_after))
        worker_threads.append(unfollow_thread)
        unfollow_thread.start()


    # Wait for all worker threads to finish
    for worker_thread in worker_threads:
        worker_thread.join()

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
