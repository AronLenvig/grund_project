import tkinter as tk
import customtkinter as ctk
import data.db_context as db
from CTKFrames.ChildrensLogin import ChildrensLogin
from CTKFrames.ChildrenSelector import ChildrenSelector
from CTKFrames.NotesFrame import NotesFrame
from CTKFrames.OverviewFrame import OverviewFrame
from datetime import datetime, timedelta
import utility as util

class ParentClient(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        #variables
        self.parent_name = ""
        self.parent_id = 0
        self.current_selected_child_id = 0
        self.current_selected_child_name = ""
        self.current_selected_child_division = "Nature"

        self.parent_name_label = ctk.CTkLabel(self, text=self.parent_name, font=("Arial", 34, "bold"))
        self.parent_name_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        #scrollbar for the childrens buttons
        self.children_selector = ChildrenSelector(self, label_text="Childrens", width=200)
        self.children_selector.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

        #map overviews for the week curent selected child is in
        self.map_overviews_frame = OverviewFrame(self)
        self.map_overviews_frame.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="nsew")

        #childrens login frame on the left side
        self.childrens_login = ChildrensLogin(self)
        self.childrens_login.grid(row=1, column=2, padx=10, pady=(10, 0), sticky="nsew")

        # notes frame on the right side
        self.notes_frame = NotesFrame(self, admin=False)
        self.notes_frame.grid(row=1, column=3, padx=10, pady=(10, 0), sticky="nsew")

        # button to refresh top left corner
        self.refresh_button = ctk.CTkButton(self, text="Refresh", command=self.refresh)
        self.refresh_button.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nsew")

        # change password button on the bottom left corner increase the size of the button
        self.change_password_button = ctk.CTkButton(self, text="Change password", command=self.change_password)
        self.change_password_button.grid(row=2, column=2, padx=10, pady=(10, 0), sticky="nsew")

        # logout button on the bottom right corner increase the size of the button
        self.logout_button = ctk.CTkButton(self, text="Logout", command=self.logout)
        self.logout_button.grid(row=2, column=3, padx=10, pady=(10, 0), sticky="nsew")

    def refresh(self):
        self.children_selector.update_children_view_from_selected_parents(self.parent_id)

    def login_child(self):
        db.connect()
        sucess = db.add_login_time(self.current_selected_child_id, datetime.now())
        db.close()
        for i, name in enumerate(self.children_selector.childrens):
            if name[1] == self.current_selected_child_name:
                self.children_selector.notify_circles[i].configure(bg_color="green")
        if sucess:
            self.notes_frame.add_note(f"{self.current_selected_child_name} logged in")

    def logout_child(self):
        db.connect()
        sucess = db.add_logout_time(self.current_selected_child_id, datetime.now())
        db.close()
        for i, name in enumerate(self.children_selector.childrens):
            if name[1] == self.current_selected_child_name:
                self.children_selector.notify_circles[i].configure(bg_color="red")
        if sucess:
            self.notes_frame.add_note(f"{self.current_selected_child_name} logged out")

    def update_self(self, child_id, child_name):
        self.current_selected_child_id = child_id
        self.current_selected_child_name = child_name
        self.childrens_login.childrens_label.configure(text=child_name+"\n"+self.current_selected_child_division)
        self.notes_frame.update_notes()
        self.map_overviews_frame.update_overview()
        db.connect()
        self.current_selected_child_division = db.get_division(child_id)
        db.close()

    def change_password(self):
        new_password = util.create_dialog("Password", "Change password")
        if util.verify_password(new_password):
            db.connect()
            db.update_parent_password(self.parent_id, new_password)
            db.close()

    def logout(self):
        self.app.login_selector()



            




