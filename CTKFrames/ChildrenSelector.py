import tkinter as tk
import customtkinter as ctk
import data.db_context as db
from functools import partial

class ChildrenSelector(ctk.CTkScrollableFrame):
    def __init__(self, app, label_text, width=400, height=400):
        super().__init__(app, label_text=label_text, width=width, height=height)
        self.app = app

        self.childrens = []
        self.childrens_buttons = []
        self.notify_circles = []

    
    def update_children_view_from_selected_divison(self, division: str):
        db.connect()
        self.current_selected_child_division = division
        self.childrens = db.get_childrens_in_division(division)
        self.update_children_view()
        self.app.update_self(self.childrens[0][0], self.childrens[0][1])
        db.close()

    def update_children_view(self):
        for button in self.childrens_buttons:
            button.destroy()

        for circle in self.notify_circles:
            circle.destroy()

        self.childrens_buttons = []
        self.notify_circles = []

        for i, child in enumerate(self.childrens):
            child_id = child[0]
            child_name = child[1]
            is_child_logged_in = db.is_child_logged_in(child_id)
            func_with_args = partial(self.app.update_self, child_id, child_name)
            switch = ctk.CTkButton(self, text=child_name, command=func_with_args)
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.childrens_buttons.append(switch)

            if is_child_logged_in:
                self.notify_circles.append(ctk.CTkLabel(self, text=" ", bg_color="green", width=20, height=20))
                self.notify_circles[i].grid(row=i, column=1, padx=10, pady=(0, 20))
            else:
                self.notify_circles.append(ctk.CTkLabel(self, text=" ", bg_color="red", width=20, height=20))
                self.notify_circles[i].grid(row=i, column=1, padx=10, pady=(0, 20))



    def update_children_view_from_selected_parents(self, parent_id: int):
        db.connect()
        self.app.parent_id = parent_id
        self.childrens = db.get_childrens(parent_id)
        self.update_children_view()
        db.close()

        self.app.parent_name_label.configure(text=self.app.parent_name)
        self.app.update_self(self.childrens[0][0], self.childrens[0][1])
