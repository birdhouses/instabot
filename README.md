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

# Known Limitations

This project is designed to help automate Instagram interactions, such as following and unfollowing users. While it can be a useful tool, there are a few known limitations that users should be aware of:

1. Instagram Rate Limits: Instagram has strict rate limits in place to prevent automated actions that may be considered spammy or abusive. If the script is run too frequently or with too many actions in a short time, your account may be temporarily or permanently suspended.

2. Instagram API Changes: Instagram frequently updates its API and internal workings, which may lead to sudden changes in the functionality of this script. We will try to keep the project up to date, but there may be times when certain features stop working until the script is updated.

3. Target Audience Matching: This project currently focuses on following users but does not include advanced targeting or filtering options for finding and engaging with specific audiences. Users looking for a more targeted growth strategy may need to explore additional tools or methods.

4. Content Discovery and Posting: This project does not currently include features for discovering popular content, filtering content based on quality or relevance, or automating the process of uploading content to your Instagram account.

5. Account Security: While the script uses the official Instagram API, automating account actions carries a certain level of risk, especially if they violate Instagram's terms of service. Use this script at your own risk and ensure you're familiar with Instagram's policies before proceeding.

6. Advanced Targeting: The script lacks advanced targeting options, such as filtering users based on interests, demographics, or engagement metrics.

7. Post Liking and Commenting: The project does not currently include the ability to automatically like and comment on posts based on specific criteria.

8. Direct Messaging: There is no functionality to automate sending direct messages to users, whether for promotional purposes or engagement.

9. Analytics and Reporting: The project does not provide analytics or reporting tools to help users track the performance and impact of their automated actions on Instagram.

10. Scheduling and Publishing Posts: The script does not have a built-in feature for scheduling and automatically publishing posts to your Instagram account.

Please note that these features may be added or improved in the future. We welcome any contributions from the community to help implement these functionalities and enhance the project's capabilities.
