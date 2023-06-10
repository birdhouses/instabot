import customtkinter
from gui.account_config import AccountConfigFrame
from gui import utils
import os

class ScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

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
            ('avoid duplicates', 'checkbox', 'avoid_duplicates'),
            ('request timeout', 'entry', 'request_timeout'),
            ('post requirements', 'checkbox', 'post_requirements_enabled'),
            ('min likes', 'entry', 'post_min_likes'),
            ('min comments', 'entry', 'post_min_comments'),
            ('detect caption language', 'checkbox', 'post_detect_caption_language'),
            ('caption languages (separeted by comma: en, nl, etc.)', 'entry', 'post_caption_languages'),
            ('post types (seperated by comma (photo, video, reel, igtv, album))', 'entry', 'post_types'),
            ('autor requirements', 'checkbox', 'post_autor_requirements_enabled'),
            ('biography keywords (seperated by comma: word1, word2)', 'entry', 'post_biography_keywords'),
            ('detect biography keywords', 'checkbox', 'post_detect_biography_keywords'),
            ('detect biography language', 'checkbox', 'post_detect_biography_language'),
            ('biography languages (separeted by comma: en, nl, etc.)', 'entry', 'post_biography_languages'),
            ('min followers', 'entry', 'post_min_followers'),
            ('max following', 'entry', 'post_max_following')
        })
        self.media_auto_discovery_frame.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.upload_posts_frame = AccountConfigFrame(self, frame_title='upload posts', fields={
            ('enabled', 'checkbox', 'enabled'),
            ('amount per day', 'entry', 'amount_per_day'),
            ('posts_dir', 'entry', 'posts_dir'),
            ('delete file after upload', 'checkbox', 'delete_after_upload'),
            ('caption (multiple captions not supported yet)', 'entry', 'caption')
        })
        self.upload_posts_frame.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.download_posts_from_account_frame = AccountConfigFrame(
            self,
            frame_title='download posts from account',
            fields={
                ('enabled', 'checkbox', 'enabled'),
                ('from account', 'entry', 'source_account'),
                ('amount', 'entry', 'amount'),
                ('request timeout', 'entry', 'timeout')
        })
        self.download_posts_from_account_frame.grid(row=7, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.button = customtkinter.CTkButton(self, text="show config", command=self.show_configured_data)
        self.button.grid(row=8, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def show_configured_data(self):
        data = utils.collect_configured_data(self)
        print(data)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.attributes('-zoomed', True)

        theme_path = os.path.abspath('./gui/themes/main_theme.json')
        utils.create_gui_window(self,
                                theme_path=theme_path,
                                title='Account configurator',
                                geometry='1920x1080',
                                column_weight=1
                                )
        self.scrollable_frame = ScrollableFrame(self, width=1920, height=1080)
        self.scrollable_frame.grid(row=0, column=0, padx=10, pady=(10,0))


        self.mainloop()

    def show_configured_data(self):
        data = utils.collect_configured_data(self)
        print(data)
