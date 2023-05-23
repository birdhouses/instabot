import customtkinter
from gui.account_config import AccountConfigFrame
from gui.utils import create_gui_window

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # TODO: load theme from path with relative path
        # This code doesn't work yet because you need to provide absolute path to theme file
        # theme_path = '/instabot/src/gui/themes/main_theme.json'
        theme_path = None
        create_gui_window(self, theme_path=theme_path)

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

        self.button = customtkinter.CTkButton(self, text="show config", command=self.button_callback)
        self.button.grid(row=5, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        self.mainloop()

    def collect_data(self):
        data = []

        account_details = self.account_config_frame.get()
        data.append(['account_details', account_details])

        use_proxies = self.use_proxies_frame.get()
        data.append(['use_proxies', use_proxies])

        follow_users = self.follow_users_frame.get()
        data.append(['follow_users', follow_users])

        unfollow_users = self.unfollow_users_frame.get()
        data.append(['unfollow_users', unfollow_users])

        return data

    def button_callback(self):
        data = self.collect_data()
        print(data)
