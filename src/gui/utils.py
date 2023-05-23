import customtkinter

def create_gui_window(self: customtkinter.CTk, theme_path = None):
    if theme_path is not None:
        customtkinter.set_default_color_theme(theme_path)
    self.title("Account config")
    self.geometry("1920x1080")
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(0, weight=0)

def collect_configured_data(self):
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

def show_configured_data(self):
        data = collect_configured_data(self)
        print(data)