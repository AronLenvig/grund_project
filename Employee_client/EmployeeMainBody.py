import tkinter as tk
import customtkinter as ctk
import data.db_context as db
from CTKFrames.ChildrensLogin import ChildrensLogin
from CTKFrames.ChildrenSelector import ChildrenSelector
from CTKFrames.NotesFrame import NotesFrame
from CTKFrames.OverviewFrame import OverviewFrame
from datetime import datetime, timedelta

class EmployeeMainBody(ctk.CTkFrame):
    def __init__(self, app, height=400, width=400):
        super().__init__(app, height=height, width=width)
        self.app = app

        #variables
        self.parent_name = ""
        self.parent_id = 0
        self.current_selected_child_id = 0
        self.current_selected_child_name = ""
        self.current_selected_child_division = "Nature"

        #scrollbar for the childrens buttons
        self.children_selector = ChildrenSelector(self, label_text="Childrens", width=200, height=400)
        self.children_selector.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        #map overviews for the week curent selected child is in
        self.map_overviews_frame = OverviewFrame(self, width=200, height=400)
        self.map_overviews_frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")

        #childrens login frame on the left side
        self.childrens_login = ChildrensLogin(self, width=200, height=400)
        self.childrens_login.grid(row=0, column=2, padx=10, pady=(10, 0), sticky="nsew")

        # notes frame on the right side
        self.notes_frame = NotesFrame(self, width=200, height=400, admin=True)
        self.notes_frame.grid(row=0, column=3, padx=10, pady=(10, 0), sticky="nsew")

        # button to refresh top left corner
        self.refresh_button = ctk.CTkButton(self, text="Refresh", command=self.refresh)
        self.refresh_button.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.children_selector.update_children_view_from_selected_divison(self.current_selected_child_division)

    def change_division(self, division):
        self.current_selected_child_division = division
        self.children_selector.update_children_view_from_selected_divison(division)

    def refresh(self):
        self.children_selector.update_children_view_from_selected_divison(self.current_selected_child_division)

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

            




