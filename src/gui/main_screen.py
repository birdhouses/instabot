import customtkinter
from gui.account_config import AccountConfigFrame
from gui import utils
import os

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        theme_path = os.path.abspath('./gui/themes/main_theme.json')

        utils.create_gui_window(self, theme_path=theme_path)

        self.account_config_frame = AccountConfigFrame(self, frame_title='account details', fields={
            ('username', 'entry', 'username'),
            ('password', 'entry', 'password')
        })
        self.account_config_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.use_proxies_frame = AccountConfigFrame(self, frame_title='proxies', fields={
            ('use proxies', 'checkbox', 'use_proxy'),
        })
        self.use_proxies_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.follow_users_frame = AccountConfigFrame(self, frame_title='follow users', fields={
            ('enabled', 'checkbox', 'enabled'),
            ('amount per day', 'entry', 'follows_per_day'),
            ('from account', 'entry', 'source_account'),
            ('like posts after following', 'checkbox', 'like_recent_posts'),
            ('amount to like', 'entry', 'like_count')
        })
        self.follow_users_frame.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.unfollow_users_frame = AccountConfigFrame(self, frame_title='unfollow users', fields={
            ('enabled', 'checkbox', 'enabled'),
            ('unfollow after (d-h-m-s)', 'entry', 'unfollow_after'),
        })
        self.unfollow_users_frame.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.comment_on_posts_frame = AccountConfigFrame(self, frame_title='comment on posts', fields={
            ('enabled', 'checkbox', 'enabled'),
            ('comment on tag', 'entry', 'comment_on_tag'),
            ('amount per day', 'entry', 'amount_per_day'),
            ('comments', 'entry', 'comments')
        })
        self.comment_on_posts_frame.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.media_auto_discovery_frame = AccountConfigFrame(self, frame_title='media auto discovery', fields={
            ('enabled', 'checkbox', 'enabled'),
            ('from tag', 'entry', 'from_tag'),
            ('amount per day', 'entry', 'amount_per_day'),
            ('save captions', 'checkbox', 'save_captions'),
            ('request timeout', 'entry', 'request_timeout')
        })
        self.media_auto_discovery_frame.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.button = customtkinter.CTkButton(self, text="show config", command=self.show_configured_data)
        self.button.grid(row=5, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        self.mainloop()

    def show_configured_data(self):
        data = utils.collect_configured_data(self)
        print(data)