import tkinter as tk
import customtkinter as ctk
import data.db_context as db


class ChildrensLogin(ctk.CTkFrame):
    def __init__(self, app, width=400, height=400):
        super().__init__(app, width=width, height=height)
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        

        #label current selected child on the top middle with division
        self.childrens_label = ctk.CTkLabel(self, text="selected child\ndivison", font=("Arial", 20, "bold"))
        self.childrens_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="nsew")

        # child login button in the middle of the screen
        self.child_login_button = ctk.CTkButton(self, text="IN", command=self.app.login_child)
        self.child_login_button.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

        # child logout button in the middle of the screen
        self.child_logout_button = ctk.CTkButton(self, text="OUT", command=self.app.logout_child)
        self.child_logout_button.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="nsew")