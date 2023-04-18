from instagrapi import Client
import instagrapi.exceptions
import instaloader
import random
import logging
import time
import json

logger = logging.getLogger()

def follow_users(cl, config, followers):
    follow_interval = config['follow_interval']
    followed_users = []
    for i, user in enumerate(followers):
        time.sleep(random.randint(follow_interval[0], follow_interval[1]))
        print(f"Followed user {user}")
        cl.user_follow(user)
        followed_users.append(user)

    return followed_users

def unfollow_users(cl, users_to_unfollow, config):
    unfollow_interval = config['unfollow_interval']
    for user in users_to_unfollow:
        time.sleep(random.randint(unfollow_interval[0], unfollow_interval[1]))
        cl.user_unfollow(user)
        logger.info(f"Unfollowed user {user.username}")

def login_user(USERNAME, PASSWORD):
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    cl = Client()
    session = cl.load_settings("session.json")

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except instaloader.LoginRequiredException:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(USERNAME, PASSWORD)
            print("Logged in using session information.")
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % USERNAME)
            if cl.login(USERNAME, PASSWORD):
                print("Logged in using username and password.")
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

    return cl

def main():
    with open('config.json', 'r') as file:
        config = json.load(file)

    username = config['account']['username']
    password = config['account']['password']
    # Run once
    cl = Client()
    cl.login(username, password)
    cl.dump_settings("session.json")
    cl = login_user(username, password)
    while True:
        source_accounts = config['source_accounts']
        for account in source_accounts:
            user_id = cl.user_id_from_username(account)
            followers = cl.user_followers(user_id, True, config['daily_follow_limit']).keys()

            users_to_unfollow = follow_users(cl, config, followers)

            print(f"Sleep for {((config['unfollow_after'] / 60) / 60)} hours")
            time.sleep(config['unfollow_after'])

            unfollow_users(cl, users_to_unfollow, config)

if __name__ == "__main__":
    main()
