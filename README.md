# Instagram Bot

This Instagram Bot is a Python script designed to automate the process of managing Instagram account(s). It uses the instagrapi library to interact with the Instagram API.

Please note that using automated scripts to interact with Instagram can be against their terms of service, and your account may be at risk of being temporarily or permanently banned. Use this script at your own risk.

### Current Features
- Follow users from specified source accounts
- Follow a configurable number of users daily

### Prerequisites

- Python 3.6+
- instagrapi library

### Installation

Clone this repository:

bash

    git clone https://github.com/birdhouses/instabot.git
    cd instabot

Install the required Python packages:

    pip install -r requirements.txt

Create a config.json file with your Instagram account credentials and desired settings (refer to the config.example.json file for an example configuration):
   
    "accounts": A list of Instagram accounts the bot will manage.
        "username": The username of the Instagram account.
        "password": The password of the Instagram account.

    "follow_users": Settings for the bot's follow/unfollow actions.
        "enabled": Set to true to enable follow/unfollow actions, or false to disable.
        "follows_per_day": The number of users the bot will follow per day.
        "unfollow_after": The time (in seconds) the bot will wait before unfollowing a user.
        "source_account": The Instagram account the bot will use as a source for finding users to follow.
        "engagement": Settings for engaging with the users the bot follows.
            "like_recent_posts": Set to true for the bot to like recent posts of the followed users, or false to disable this feature.
            "like_count": The number of recent posts the bot will like for each followed user.

### Usage

Run the script:

    python3 main.py

The script will start following users from the specified source accounts, with a limit of users followed daily, and random intervals between follow actions.

After the specified unfollow_after time interval, the bot will start unfollowing users it previously followed, with random intervals between unfollow actions.

The script will keep running indefinitely, repeating the follow and unfollow process.
