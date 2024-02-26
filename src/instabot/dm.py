from instagrapi import Client
from typing import Dict, Any
from instabot.timekeeper import TimeKeeper
from instabot import utils
import asyncio

async def dm_from_list(cl: Client, account: Dict[str, Any]):
    amount = account['dm_accounts_from_list']['timeout']
    username = account['account_details']['username']
    message = account['dm_accounts_from_list']['message']

    for _account in account['dm_accounts_from_list']['accounts']:
        TimeKeeper(username, 'dm_account', amount)

        await asyncio.sleep(amount)

        send_dm(client=cl, username=_account, message=message)

def send_dm(client: Client, username: str, message: str):
    """
    Send a direct message to a specified user using the instagrapi client.

    :param client: An authenticated instagrapi Client instance.
    :param username: The username of the recipient.
    :param message: The message text to be sent.
    """
    user_id = client.user_id_from_username(username)
    client.direct_send(message, [user_id])
