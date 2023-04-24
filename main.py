import instabot
import threading

def run_bot(account):
    username = account['username']
    password = account['password']

    cl = instabot.get_client(username, password)

    while True:
        if account['follow_users']['enabled']:
            instabot.follow_user_followers(cl, account)

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
