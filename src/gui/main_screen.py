import customtkinter
from gui.account_config import AccountConfigFrame
from gui.utils import ConfigManager
import os
import json

class ScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, account=None, parent=None, **kwargs):
        super().__init__(master, **kwargs)
        self.gui = self
        self.parent = parent

        def get_default_value(keys):
            value = account
            for key in keys:
                if value is None:
                    return None
                value = value.get(key)
            return value

        self.account_details_frame = AccountConfigFrame(self, frame_title='account details', fields=[
            ('username', 'entry', 'username', get_default_value(['account_details', 'username'])),
            ('password', 'entry', 'password', get_default_value(['account_details', 'password']))
        ])
        self.account_details_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.use_proxies_frame = AccountConfigFrame(self, frame_title='proxies', fields=[
            ('use proxies', 'checkbox', 'use_proxy', get_default_value(['use_proxies', 'use_proxy'])),
        ])
        self.use_proxies_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.follow_users_frame = AccountConfigFrame(
            self,
            frame_title='follow users',
            fields=[
            ('enabled', 'checkbox', 'enabled', get_default_value(['follow_users', 'enabled'])),
            ('amount per day', 'entry', 'follows_per_day', get_default_value(['follow_users', 'follows_per_day'])),
            ('from account', 'entry', 'source_account', get_default_value(['follow_users','source_account'])),
            [
                'engagement',
                ('like posts after following', 'checkbox', 'like_recent_posts', get_default_value(['follow_users', 'engagement', 'like_recent_posts'])),
                ('amount to like', 'entry', 'like_count', get_default_value(['follow_users', 'engagement', 'like_count'])),
            ]
        ])
        self.follow_users_frame.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.unfollow_users_frame = AccountConfigFrame(self, frame_title='unfollow users', fields=[
            ('enabled', 'checkbox', 'enabled', get_default_value(['unfollow_users', 'enabled'])),
            ('unfollow after (d-h-m-s)', 'entry', 'unfollow_after', get_default_value(['unfollow_users', 'unfollow_after'])),
        ])
        self.unfollow_users_frame.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.comment_on_media_frame = AccountConfigFrame(self, frame_title='comment on media', fields=[
            ('enabled', 'checkbox', 'enabled', get_default_value(['comment_on_media', 'enabled'])),
            ('comment on tag', 'entry', 'comment_on_tag', get_default_value(['comment_on_media', 'comment_on_tag'])),
            ('amount per day', 'entry', 'amount_per_day', get_default_value(['comment_on_media', 'amount_per_day'])),
            ('comments (separated by newline)', 'textarea', 'comments', get_default_value(['comment_on_media', 'comments']))
        ])
        self.comment_on_media_frame.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.upload_posts_frame = AccountConfigFrame(self, frame_title='upload posts', fields=[
            ('enabled', 'checkbox', 'enabled', get_default_value(['upload_posts', 'enabled'])),
            ('amount per day', 'entry', 'amount_per_day', get_default_value(['upload_posts', 'amount_per_day'])),
            ('posts_dir', 'entry', 'posts_dir', get_default_value(['upload_posts', 'posts_dir'])),
            ('delete file after upload', 'checkbox', 'delete_after_upload', get_default_value(['upload_posts', 'delete_after_upload'])),
            ('caption (separated by newline)', 'textarea', 'caption', get_default_value(['upload_posts', 'caption'])),
            ('captions file', 'entry', 'captions_file', get_default_value(['upload_posts', 'captions_file']))  # New field
        ])
        self.upload_posts_frame.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.upload_stories_frame = AccountConfigFrame(self, frame_title='upload stories', fields=[
            ('enabled', 'checkbox', 'enabled', get_default_value(['upload_stories', 'enabled'])),
            ('amount per day', 'entry', 'amount_per_day', get_default_value(['upload_stories', 'amount_per_day'])),
            ('posts_dir', 'entry', 'posts_dir', get_default_value(['upload_stories', 'posts_dir'])),
            ('delete file after upload', 'checkbox', 'delete_after_upload', get_default_value(['upload_stories', 'delete_after_upload'])),
            ('caption (separated by newline)', 'textarea', 'caption', get_default_value(['upload_stories', 'caption'])),
            ('captions file', 'entry', 'captions_file', get_default_value(['upload_stories', 'captions_file']))  # New field
        ])
        self.upload_stories_frame.grid(row=7, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.download_posts_from_account_frame = AccountConfigFrame(
            self,
            frame_title='download posts from account',
            fields=[
                ('enabled', 'checkbox', 'enabled', get_default_value(['download_posts_from_account', 'enabled'])),
                ('from account', 'entry', 'source_account', get_default_value(['download_posts_from_account','source_account'])),
                ('path to save to', 'entry', 'save_path', get_default_value(['download_posts_from_account', 'save_path'])),
                ('amount', 'entry', 'amount', get_default_value(['download_posts_from_account', 'amount'])),
                ('request timeout', 'entry', 'timeout', get_default_value(['download_posts_from_account','timeout']))
        ])
        self.download_posts_from_account_frame.grid(row=8, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.dm_accounts_from_list_frame = AccountConfigFrame(
            self,
            frame_title='DM accounts from specified list',
            fields=[
                ('enabled', 'checkbox', 'enabled', get_default_value(['dm_accounts_from_list', 'enabled'])),
                ('message', 'textarea', 'message', get_default_value(['dm_accounts_from_list', 'message'])),
                ('accounts (separated by newline)', 'textarea', 'accounts', get_default_value(['dm_accounts_from_list', 'accounts'])),
                ('request timeout', 'entry', 'timeout', get_default_value(['dm_accounts_from_list','timeout']))
        ])
        self.dm_accounts_from_list_frame.grid(row=9, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.button = customtkinter.CTkButton(self, text="Add account", command=self.show_configured_data)
        self.button.grid(row=10, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def show_configured_data(self):
        config_manager = ConfigManager(self.gui)
        data = config_manager.collect_configured_data()
        config_manager.write_to_config(data, menu=self.parent)

class App(customtkinter.CTk):
    def __init__(self, account=None, parent=None):
        super().__init__()

        # TODO: make this configurable & fix window resizing
        width, height = 1920, 1080

        theme_path = os.path.abspath('./gui/themes/main_theme.json')
        ConfigManager.create_gui_window(self,
                                theme_path=theme_path,
                                title='Account configurator',
                                geometry=f'{width}x{height}',
                                column_weight=0
                                )

        frame_width = width * 0.95
        frame_height = height * 0.8

        self.scrollable_frame = ScrollableFrame(self, width=frame_width, height=frame_height, account=account, parent=parent)
        self.scrollable_frame.grid(row=0, column=0, padx=10, pady=(10,0))

        self.mainloop()
