# InstaBot
Automate your instagram account management using this bot. Fill in your requirements in the config.json file and run the script! You can configure multiple accounts which will run simutanously.

Please note that using automated scripts to interact with Instagram can be against their terms of service, and your account may be at risk of being temporarily or permanently banned. Use this bot at your own risk.

### Supporting the project
Please consider donating to support development of the project

[![Become a Patron](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://www.patreon.com/birdhouses) <br>

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a-Coffee-orange)](https://www.buymeacoffee.com/birdhouses) <br>


## Current Features
- Follow users from specified source accounts
- Unfollow users after a configured amount of time
- Follow a configurable number of users daily
- Post comments on recent posts by a specified hashtag
- Like a number of posts after following a user
- Using multiple accounts at the same time
- Proxy support for making requests
- Automatically download posts from a specified tag, based on user requirements
- Upload a configured amount of posts each day

## Proxy configuration
In the main directory of your Instagram Bot, create a file named proxies.txt. Each line in this file should represent a single proxy in the format IP:Port:Username:Password. For example:

    123.45.67.89:8080:user1:pass1
    98.76.54.32:8080:user2:pass2


## Prerequisites

- Python 3.11+

## Installation

Clone this repository:

    git clone https://github.com/birdhouses/instabot.git
    cd instabot

Install the required Python packages:

    pip install -r requirements.txt

Create a config.json file with your Instagram account credentials and desired settings (refer to the config.example.json file for an example configuration)


# Usage
## Uploading posts
In order to upload posts you need to specify the source directory of where the files to be posted are stored.
For example if you want to upload posts from the `/src/posts` folder (you'd need to create the `/posts` folder manually) then specify it as follows in the `config.json` file:

    "upload_posts": {
        "enabled": true,
        "amount_per_day": 3,
        "posts_dir": "./posts",
        "delete_after_upload": true,
        "caption": "Cool caption.."
      },
The folder structure for the files to be depends on if you want to upload single posts or albums. Here is an example configuration that will upload 1 single post and 1 album containing 2 pictures:

    /posts
        /image_1.jpg
        /album_1
            /image_1.jpg
            /image_2.jpg

Run the script:

    /instabot/src python3.11 main.py

