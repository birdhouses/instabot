import customtkinter

def create_gui_window(self: customtkinter.CTk, theme_path = None):
    if theme_path is not None:
        customtkinter.set_default_color_theme(theme_path)
    self.title("Account config")
    self.geometry("1920x1080")
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(0, weight=0)