# Instagram Bot

This Instagram Bot is a Python script designed to automate the process of managing Instagram account(s). It uses the instagrapi library to interact with the Instagram API.

Please note that using automated scripts to interact with Instagram can be against their terms of service, and your account may be at risk of being temporarily or permanently banned. Use this script at your own risk.

Current Features

- Follow users from specified source accounts
- Follow a configurable number of users daily
- Unfollow users after a specified time interval
- Random intervals between follow and unfollow actions
- Logging of followed and unfollowed users

# Prerequisites

- Python 3.6+
- instagrapi library

# Installation

Clone this repository:

bash

    git clone https://github.com/your-username/instagram-follow-bot.git
    cd instagram-follow-bot

Install the required Python packages:

    pip install -r requirements.txt

Create a config.json file with your Instagram account credentials and desired settings (refer to the config.example.json file for an example configuration):

json

        {
          "account": {
            "username": "your_username",
            "password": "your_password"
          },
          "source_accounts": [
            "source_account1",
            "source_account2"
          ],
          "daily_follow_limit": 100,
          "unfollow_after": 86400,
          "follow_interval": [10, 20],
          "unfollow_interval": [10, 20]
        }

# Usage

Run the script:

    python followbot.py

The script will start following users from the specified source accounts, with a limit of users followed daily, and random intervals between follow actions.

After the specified unfollow_after time interval, the bot will start unfollowing users it previously followed, with random intervals between unfollow actions.

The script will keep running indefinitely, repeating the follow and unfollow process.

# Logs

The script uses the Python logging module to log its actions, such as following and unfollowing users. By default, the log messages are printed to the console. If you want to save the logs to a file, you can modify the logger configuration in the followbot.py script:

python

    logger.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logger.INFO,
        handlers=[
            logger.StreamHandler(),
            logger.FileHandler("followbot.log")  # Add this line to log messages to a file
        ]
    )

This will save the log messages to a file named followbot.log in the same directory as the script.
