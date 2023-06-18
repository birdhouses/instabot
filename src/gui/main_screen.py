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
            ('comments (seperated by newline)', 'textarea', 'comments', get_default_value(['comment_on_media', 'comments']))
        ])
        self.comment_on_media_frame.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.media_auto_discovery_frame = AccountConfigFrame(self, frame_title='media auto discovery', fields=[
            ('enabled', 'checkbox', 'enabled', get_default_value(['media_auto_discovery', 'enabled'])),
            ('from tag', 'entry', 'from_tag', get_default_value(['media_auto_discovery', 'from_tag'])),
            ('amount per day', 'entry', 'amount_per_day', get_default_value(['media_auto_discovery', 'amount_per_day'])),
            ('save captions', 'checkbox', 'save_captions', get_default_value(['media_auto_discovery','save_captions'])),
            ('avoid duplicates', 'checkbox', 'avoid_duplicates', get_default_value(['media_auto_discovery', 'avoid_duplicates'])),
            ('request timeout', 'entry', 'request_timeout', get_default_value(['media_auto_discovery', 'request_timeout'])),
            [
                'post_requirements',
                ('min likes', 'entry', 'min_likes', get_default_value(['media_auto_discovery', 'post_requirements','min_likes'])),
                ('min comments', 'entry', 'min_comments', get_default_value(['media_auto_discovery', 'post_requirements','min_comments'])),
                ('detect caption language', 'checkbox', 'detect_caption_language', get_default_value(['media_auto_discovery', 'post_requirements', 'detect_caption_language'])),
                ('caption languages (separeted by newline', 'textarea', 'languages', get_default_value(['media_auto_discovery', 'post_requirements', 'languages'])),
                ('post types (seperated by newline)', 'textarea', 'allowed_post_types', get_default_value(['media_auto_discovery', 'post_requirements', 'allowed_post_types'])),
            ],
            [
                'author_requirements',
                ('enabled', 'checkbox', 'enabled', get_default_value(['media_auto_discovery', 'author_requirements', 'enabled'])),
                ('biography keywords (seperated by newline)', 'textarea', 'biography_keywords', get_default_value(['media_auto_discovery', 'author_requirements', 'biography_keywords'])),
                ('detect biography keywords', 'checkbox', 'detect_biography_keywords', get_default_value(['media_auto_discovery', 'author_requirements', 'detect_biography_keywords'])),
                ('detect biography language', 'checkbox', 'detect_biography_language', get_default_value(['media_auto_discovery', 'author_requirements', 'detect_biography_language'])),
                ('biography languages (separeted by newline)', 'textarea', 'languages', get_default_value(['media_auto_discovery', 'author_requirements', 'languages'])),
                ('min followers', 'entry', 'min_followers', get_default_value(['media_auto_discovery', 'author_requirements','min_followers'])),
                ('max following', 'entry', 'max_following', get_default_value(['media_auto_discovery', 'author_requirements','max_following'])),
            ]
        ])
        self.media_auto_discovery_frame.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.upload_posts_frame = AccountConfigFrame(self, frame_title='upload posts', fields=[
            ('enabled', 'checkbox', 'enabled', get_default_value(['upload_posts', 'enabled'])),
            ('amount per day', 'entry', 'amount_per_day', get_default_value(['upload_posts', 'amount_per_day'])),
            ('posts_dir', 'entry', 'posts_dir', get_default_value(['upload_posts', 'posts_dir'])),
            ('delete file after upload', 'checkbox', 'delete_after_upload', get_default_value(['upload_posts', 'delete_after_upload'])),
            ('caption (seperated by newline)', 'textarea', 'caption', get_default_value(['upload_posts', 'caption']))
        ])
        self.upload_posts_frame.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="ew")

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
        self.download_posts_from_account_frame.grid(row=7, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.button = customtkinter.CTkButton(self, text="Add account", command=self.show_configured_data)
        self.button.grid(row=8, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

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