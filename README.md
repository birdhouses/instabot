# InstaBot
Automate your instagram account management using this bot. Fill in your requirements in the config.json file and run the script! You can configure multiple accounts which will run simutanously.

Please note that using automated scripts to interact with Instagram can be against their terms of service, and your account may be at risk of being temporarily or permanently banned. Use this bot at your own risk.

### Supporting the project
Please consider donating to support development of the project

[![Become a Patron](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://www.patreon.com/birdhouses) <br>

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a-Coffee-orange)](https://www.buymeacoffee.com/birdhouses) <br>


## Current Features
- Automated posting
- Automated stories
- Automated Direct Messaging (mass DM's)
- Follow / unfollowing
- Post comments on recent posts by a specified hashtag
- Using multiple accounts at the same time
- Proxy support for making requests (unstable)


## Prerequisites

- Python 3.11+

## Installation

Clone this repository:

    git clone https://github.com/birdhouses/instabot.git
    cd instabot

Install the required Python packages:

    pip install -r requirements.txt

# Usage guide
### Run the bot:
Open the GUI

    /instabot/src python3.11 gui.py

If you want to run the without the gui, you can run

    /instabot/src python3.11 main.py

### Using GUI to add accounts
In a terminal navigate to ```/instabot/src``` and run ```gui.py```. A window will open where you fill in your required configurations. After you're done simply click on the "Add account" button and a new file called ```config.json``` will be created in the ```/src``` directory with the account data.
If you accidentally added a account, you may manually remove it from the ```config.json``` file.

Please note that this feature is still under development. Feel free to create an issue in the github repo with any errors you encounter.

## DM Automation
To send automatically send DMs to users you need to manually specify a list of usernames to send the DM's to. Using the GUI, each username must be on a newline in the textarea.
You can also modify the config.json manually, and provide an array of usernames in the `dm_accounts_from_list.accounts` setting. You can set the `timeout` in seconds between each DM. 
You can specify the `message`. This needs to be a single-line string.

## Proxy configuration
In the main directory of your Instagram Bot, create a file named proxies.txt. Each line in this file should represent a single proxy in the format IP:Port:Username:Password. For example:

    123.45.67.89:8080:user1:pass1
    98.76.54.32:8080:user2:pass2

### Uploading posts
In order to upload posts you need to specify the source directory of where the files to be posted are stored.
For example if you want to upload posts from the `/src/posts` folder (you'd need to create the `/posts` folder manually) then specify it as follows in the `config.json` file:

    "upload_posts": {
        "enabled": true,
        "amount_per_day": 3,
        "posts_dir": "./posts",
        "delete_after_upload": true,
        "caption": "Cool caption.."
      },
The folder structure for the files to be depends on if you want to upload single posts or albums. Here is an example folder structure that will upload 1 single post and 1 album containing 2 pictures:

    /posts
        /image_1.jpg
        /album_1
            /image_1.jpg
            /image_2.jpg
            
### Uploading stories
For example if you want to upload posts from the `/src/posts` folder (you'd need to create the `/posts` folder manually) then specify it as follows in the `config.json` file:

    "upload_stories": {
        "enabled": true,
        "amount_per_day": 3,
        "posts_dir": "./posts",
        "delete_after_upload": true,
        "caption": "Cool caption.."
      },
Example folder structure:

    /posts
        /image_1.jpg
        /video_1.mp4
        
### Downloading posts from a specified instagram account
To download posts from one instagram account, you need to specify the username of the instagram account in the `config.json` file:

    "download_posts_from_account": {
          "enabled": false,
          "save_path": "./posts",
          "source_account": "instagram",
          "amount": 5,
          "timeout": 2
        }
Make sure the `source_account` is public. You can specify the amount of posts you want to download, and the timeout between each download.
It should be noted that this task does not use authentication, which means that it is not possible to use proxies for this task. (Because the get_client method handles authentication & proxies properly).

### Commenting on posts
To comment on posts from a specified tag you can use the following settings:

    "comment_on_media": {
            "enabled": false,
            "comment_on_tag": "memes",
            "amount_per_day": 10,
            "comments": [
                "Intresting comment",
                "Intresting comment 2"
            ]
            },
This will automatically comment on 10 posts from a specified tag each day and select a random comment from the list of comments to comment.

