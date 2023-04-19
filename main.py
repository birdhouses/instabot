import instabot
import json
import time

def main():
    with open('config.json', 'r') as file:
        config = json.load(file)

    username = config['account']['username']
    password = config['account']['password']
    # Run once
    cl = instabot.login_user(username, password)

    while True:
        source_accounts = config['source_accounts']

        for account in source_accounts:
            user_id = cl.user_id_from_username(account)
            followers = cl.user_followers(user_id, True, config['daily_follow_limit']).keys()

            users_to_unfollow = instabot.follow_users(cl, config, followers)

            print(f"Sleep for {((config['unfollow_after'] / 60) / 60)} hours")
            time.sleep(config['unfollow_after'])

            instabot.unfollow_users(cl, users_to_unfollow, config)

if __name__ == "__main__":
    main()