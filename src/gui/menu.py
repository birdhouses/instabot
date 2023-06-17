import customtkinter as ctk
import tkinter as tk
from instabot import utils
from . import main_screen
import json

class MainMenu(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self, bg='black')
        self.scrollbar = ctk.CTkScrollbar(self, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollable_frame = tk.Frame(self.canvas, bg='black')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Add title
        title_frame = tk.Frame(self.scrollable_frame, bg='black')
        title_frame.grid(sticky="ew")
        title_label = ctk.CTkLabel(title_frame, text="Accounts", font=("Arial", 30))
        title_label.grid()

    def add_account(self, account):
        account_frame = tk.Frame(self.scrollable_frame, bg='black')
        account_frame.grid(sticky="ew")

        username_label = ctk.CTkLabel(account_frame, text=account['account_details']['username'])
        username_label.grid(column=0)

        configure_button = ctk.CTkButton(account_frame, text="Configure", font=("Arial", 15), command=lambda: self.configure_account(account))
        configure_button.grid(column=1)

    def load_accounts_from_file(self):
        try:
            with open('./config.json', 'r+') as file:
                config = json.load(file)
        except FileNotFoundError:
            with open('./config.json', 'w') as file:
                config = {"accounts": []}
                json.dump(config, file)

        accounts = config['accounts']

        for account in accounts:
            self.add_account(account)

    def configure_account(self, account=None):
        main_screen.App(account=account, parent=self)

    def refresh_accounts(self):
        # Clear current accounts
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Reload accounts
        self.load_accounts_from_file()

class App():
    def __init__(self):
        super().__init__()

        root = tk.Tk()
        root.configure(bg='black')
        root.title('Instagram Bot')

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        menu = MainMenu(root)
        menu.grid(sticky="nsew")

        # Add account button outside of the table
        add_account_button = ctk.CTkButton(root, text="Add account", font=("Arial", 20), command=lambda: menu.configure_account())
        add_account_button.grid(pady=10)

        # load accounts
        menu.load_accounts_from_file()

        root.mainloop()

