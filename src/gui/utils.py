import customtkinter
import json

def create_gui_window(self: customtkinter.CTk,
                      theme_path: str = None,
                      title: str = None,
                      geometry: str = None,
                      column_count: int = 0,
                      row_count: int = 0,
                      column_weight: int = 0,
                      row_weight: int = 0,
                      ) -> None:
    if theme_path is not None:
        customtkinter.set_default_color_theme(theme_path)
    if title is not None:
        self.title(title)
    if geometry is not None:
        self.geometry(geometry)

    self.grid_columnconfigure(column_count, weight=column_weight)
    self.grid_rowconfigure(row_count, weight=row_weight)

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

        comment_on_posts = self.comment_on_posts_frame.get()
        data.append(['comment_on_posts', comment_on_posts])

        media_auto_discovery = self.media_auto_discovery_frame.get()
        data.append(['media_auto_discovery', media_auto_discovery])

        upload_posts = self.upload_posts_frame.get()
        data.append(['upload_posts', upload_posts])

        download_posts = self.download_posts_from_account_frame.get()
        data.append(['download_posts_from_account', download_posts])

        return data

def write_to_config(data: list) -> None:
    ##TODO: write to config file
    # Refactor data to be the same format as in the current config file
    # Show warning message
    # On confirm write to config file
    formatted_data = format_data(data)

    with open('test.json', 'w') as f:
        f.write(formatted_data)

def format_data(data: list) -> list:
    formatted_data = {}
    for item in data:
        for key, value in item[1]:
            if formatted_data.get(item[0]) is None:
                formatted_data[item[0]] = {}

            formatted_data[item[0]] |= {key: value}

    return json.dumps(formatted_data)
