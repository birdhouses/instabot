# Instagram Bot

This Instagram Bot is a Python script designed to automate the process of managing Instagram account(s). It uses the instagrapi library to interact with the Instagram API.

Please note that using automated scripts to interact with Instagram can be against their terms of service, and your account may be at risk of being temporarily or permanently banned. Use this script at your own risk.

### Current Features
- Follow users from specified source accounts
- Unfollow users after a configured amount of time
- Follow a configurable number of users daily
- Post comments on recent posts by a specified hashtag
- Like a number of posts after following a user

### Prerequisites

- Python 3.6+

### Installation

Clone this repository:

    git clone https://github.com/birdhouses/instabot.git
    cd instabot

Install the required Python packages:

    pip install -r requirements.txt

Create a config.json file with your Instagram account credentials and desired settings (refer to the config.example.json file for an example configuration):


### Usage

Run the script:

    python3 main.py

