import json
import customtkinter

class ConfigManager:
    def __init__(self, gui):
        self.gui = gui

    @staticmethod
    def create_gui_window(gui_instance, theme_path=None, title=None, geometry=None, column_count=0, row_count=0, column_weight=0, row_weight=0):
        if theme_path is not None:
            customtkinter.set_default_color_theme(theme_path)
        if title is not None:
            gui_instance.title(title)
        if geometry is not None:
            gui_instance.geometry(geometry)

        gui_instance.grid_columnconfigure(column_count, weight=column_weight)
        gui_instance.grid_rowconfigure(row_count, weight=row_weight)

    def collect_configured_data(self):
        data = []
        frames = [
            'account_config_frame',
            'use_proxies_frame',
            'follow_users_frame',
            'unfollow_users_frame',
            'comment_on_posts_frame',
            'media_auto_discovery_frame',
            'upload_posts_frame',
            'download_posts_from_account_frame'
        ]
        for frame in frames:
            frame_data = getattr(self.gui, frame).get()
            data.append([frame.replace('_frame', ''), frame_data])
        return data

    def write_to_config(self, data, filename='test.json'):
        new_account = self.format_data(data)
        try:
            with open(filename, 'r+') as f:
                config = json.load(f)
                config['accounts'].append(new_account)
                f.seek(0)
                f.write(json.dumps(config, indent=4))
                f.truncate()
        except FileNotFoundError:
            with open(filename, 'w+') as f:
                config = {'accounts': [new_account]}
                f.write(json.dumps(config, indent=4))

    def format_data(self, data: list) -> str:
        formatted_data = {}

        for item in data:
            key = item[0]
            value = item[1]

            if isinstance(value, list):  # Handle nested fields
                nested_dict = {}
                for nested_item in value:
                    nested_key = nested_item[0]
                    nested_value = nested_item[1]

                    # Check if the value is another nested list
                    if isinstance(nested_value, list):
                        nested_value = {i[0]: convert_value(i[1]) for i in nested_value}

                    nested_dict[nested_key] = convert_value(nested_value)

                formatted_data[key] = nested_dict
            else:
                formatted_data[key] = convert_value(value)

        return formatted_data

def convert_value(value):
    # Convert the string values to their appropriate types
    if isinstance(value, str):
        if value.isdigit():
            value = int(value)
        elif value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
    return value
