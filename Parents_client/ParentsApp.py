import tkinter as tk
import customtkinter as ctk
import Parents_client.ParentLogin as ParentLogin
import Parents_client.ParentClient as ParentClient
import os

ctk.set_appearance_mode("system")  # Modes: system (default), light, dark
ctk.set_default_color_theme("dark-blue") # Themes: blue (default), dark-blue, green
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.parent_login = ParentLogin.ParentLogin(self)
        self.parent_client = ParentClient.ParentClient(self)
        self.login_selector()

    def login_selector(self):
        self.parent_client.pack_forget()
        self.geometry(f"{500}x{580}")
        self.resizable(False, False)
        self.title("Login Parents Client")
        self.parent_login.pack(in_=self, fill=tk.BOTH, expand=True, padx=0, pady=0)

    def main_selector(self):
        self.parent_login.pack_forget()
        self.geometry(f"{1200}x{580}")
        self.resizable(False, False)

        self.title("Parents Client")
        self.parent_client.pack(in_=self, fill=tk.BOTH, expand=True, padx=0, pady=0)

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()