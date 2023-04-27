import os
import shutil
import pytest
import datetime
from instabot import (
    save_followed_user, load_followed_users,
    filter_users_to_unfollow, remove_unfollowed_user,
    mark_unfollowed_user, user_not_followed_before
)
from instagrapi import Client

def test_filter_users_to_unfollow():
    now = datetime.datetime.now()
    followed_users = [
        (11111, now - datetime.timedelta(days=2)),
        (22222, now - datetime.timedelta(hours=1)),
    ]

    follow_time = "1-0-0-0"
    users_to_unfollow = filter_users_to_unfollow(followed_users, follow_time)
    assert 11111 in users_to_unfollow
    assert 22222 not in users_to_unfollow