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
            'username': 'entry',
            'password': 'entry'
        })
        self.account_config_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.use_proxies_frame = AccountConfigFrame(self, frame_title='proxies', fields={
            'use proxies': 'checkbox',
        })
        self.use_proxies_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.follow_users_frame = AccountConfigFrame(self, frame_title='follow users', fields={
            'enabled': 'checkbox',
            'amount per day': 'entry',
            'from account': 'entry',
            'like posts after following': 'checkbox',
            'amount to like': 'entry'
        })
        self.follow_users_frame.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.unfollow_users_frame = AccountConfigFrame(self, frame_title='unfollow users', fields={
            'enabled': 'checkbox',
            'unfollow after (d-h-m-s)': 'entry',
        })
        self.unfollow_users_frame.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.comment_on_posts_frame = AccountConfigFrame(self, frame_title='comment on posts', fields={
            'enabled': 'checkbox',
            'comment on tag': 'entry',
            'amount per day': 'entry',
            'comments': 'entry'
        })
        self.comment_on_posts_frame.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.media_auto_discovery_frame = AccountConfigFrame(self, frame_title='media auto discovery', fields={
            'enabled': 'checkbox',
            'from tag': 'entry',
            'amount per day': 'entry',
            'save captions': 'checkbox',
            'request timeout': 'entry'
        })
        self.media_auto_discovery_frame.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.button = customtkinter.CTkButton(self, text="show config", command=self.show_configured_data)
        self.button.grid(row=5, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        self.mainloop()

    def show_configured_data(self):
        data = utils.collect_configured_data(self)
        print(data)
