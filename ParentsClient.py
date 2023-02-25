import tkinter
import customtkinter
import db_context as db
from functools import partial
from datetime import datetime

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue") # Themes: blue (default), dark-blue, green

class App(customtkinter.CTk):

    frames: dict[customtkinter.CTkFrame] = {}
    parent_name = ""
    parent_id = 0
    current_selected_child_id = 0
    current_selected_child_name = ""
    current_selected_child_division = ""
    notes = []
    children = []

    def __init__(self):
        super().__init__()
        # contains everything
        main_container = customtkinter.CTkFrame(self)
        main_container.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        self.main_container = customtkinter.CTkFrame(main_container)
        self.main_container.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=0, pady=0)

        # Login Frame
        App.frames['Login'] = customtkinter.CTkFrame(main_container)
        self.username_label = customtkinter.CTkLabel(App.frames['Login'], text="Username")
        self.username_label.place(relx=0.5, rely=0.35, anchor=tkinter.CENTER)

        self.username_entry = customtkinter.CTkEntry(App.frames['Login'], width=200)
        self.username_entry.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.password_label = customtkinter.CTkLabel(App.frames['Login'], text="Password")
        self.password_label.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

        self.password_entry = customtkinter.CTkEntry(App.frames['Login'], width=200, show="*")
        self.password_entry.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        self.login_button = customtkinter.CTkButton(App.frames['Login'], text="Login", command=self.login)
        self.login_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        self.error_label = customtkinter.CTkLabel(App.frames['Login'], text="",)
        self.error_label.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        self.username_entry.bind("<Return>", self.login)
        self.password_entry.bind("<Return>", self.login)
        self.username_entry.bind("<FocusIn>", lambda event: self.username_entry.configure(border_color="grey"))
        self.password_entry.bind("<FocusIn>", lambda event: self.password_entry.configure(border_color="grey"))
        self.username_entry.bind("<Button-1>", lambda event: self.username_entry.configure(border_color="grey"))
        self.password_entry.bind("<Button-1>", lambda event: self.password_entry.configure(border_color="grey"))

        # Main Frame
        App.frames['Main'] = customtkinter.CTkFrame(main_container)

        #label Parent name on the top left corner
        self.parent_name_label = customtkinter.CTkLabel(App.frames['Main'], text=App.parent_name, font=("Arial", 34, "bold"))
        self.parent_name_label.place(relx=0.01, rely=0.01, anchor=tkinter.NW)

        #label Childrens on the top middle
        self.childrens_label = customtkinter.CTkLabel(App.frames['Main'], text="Current selected child name", font=("Arial", 20, "bold"))
        self.childrens_label.place(relx=0.5, rely=0.05, anchor=tkinter.N)

        # for every child in the list of childrens, create a button on the left side
        self.childrens_buttons = []
        self.notify_circles = []
        
        # logout button on the bottom right corner
        self.logout_button = customtkinter.CTkButton(App.frames['Main'], text="Logout", command=self.login_selector)
        self.logout_button.place(relx=0.90, rely=0.95, anchor=tkinter.S)

        # child login button in the middle of the screen
        self.child_login_button = customtkinter.CTkButton(App.frames['Main'], text="Login this child", command=self.login_child)
        self.child_login_button.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

        # child logout button in the middle of the screen
        self.child_logout_button = customtkinter.CTkButton(App.frames['Main'], text="Logout this child", command=self.logout_child)
        self.child_logout_button.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

        # change password button on the bottom left corner
        self.change_password_button = customtkinter.CTkButton(App.frames['Main'], text="Change password", command=self.change_password)
        self.change_password_button.place(relx=0.01, rely=0.95, anchor=tkinter.SW)

        # add note button on the top right corner
        self.add_note_button = customtkinter.CTkButton(App.frames['Main'], text="Add note", command=self.add_note_dialog)
        self.add_note_button.place(relx=0.90, rely=0.05, anchor=tkinter.N)

        # notes frame on the right side
        self.notes_frame = customtkinter.CTkFrame(App.frames['Main'])
        self.notes_frame.place(relx=0.85, rely=0.2, anchor=tkinter.N)

        # notes scrollbar
        self.notes_scrollbar = customtkinter.CTkScrollbar(self.notes_frame)
        self.notes_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # textbox widget for notes readonly
        self.notes_text = customtkinter.CTkTextbox(self.notes_frame, width=400, height=300, yscrollcommand=self.notes_scrollbar.set, state=tkinter.DISABLED)
        self.notes_text.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

        # configure the scrollbar
        self.notes_scrollbar.configure(command=self.notes_text.yview)
        
        
        self.login_selector()

    def update_notes(self):
        db.connect()
        notes = db.get_notes_day(App.current_selected_child_id, 0)
        db.close()
        notes_text = ""
        for note in notes:
            notes_text += note[0].strftime("%H:%M:%S") + " - "
            notes_text += note[1]
            notes_text += "\n"
        
        self.notes_text.configure(state=tkinter.NORMAL)
        self.notes_text.delete(1.0, tkinter.END)
        self.notes_text.insert(tkinter.END, notes_text)
        self.notes_text.configure(state=tkinter.DISABLED)


    def add_note_dialog(self):
        dilog = self.create_dialog("add a note", "Note")
        if dilog:
            self.add_note(dilog)
    
    def add_note(self, note):
        db.connect()
        db.add_note_to_child(App.current_selected_child_id, note)
        db.close()
        self.update_notes()

    def change_password(self):
        new_password = self.create_dialog("type your new password", "Change password")

        if len(new_password) < 6:
            tkinter.messagebox.showerror("Error", "Password must be more than 6 characters")
            return
        if len(new_password) > 20:
            tkinter.messagebox.showerror("Error", "Password must be less than 20 characters")
            return
        
        db.connect()
        db.update_parent_password(App.parent_id, new_password)
        db.close()

        tkinter.messagebox.showinfo("Success", "Password changed successfully")

    def create_dialog(self, text, title):
        dialog = customtkinter.CTkInputDialog(text=text, title=title)
        return dialog.get_input()

    def login_child(self):
        db.connect()
        db.add_login_time(App.current_selected_child_id, datetime.now())
        #update the notify circle where the child name 
        for i, name in enumerate(App.childrens):
            if name[1] == App.current_selected_child_name:
                self.notify_circles[i].configure(bg_color="green")
        db.close()
        self.add_note(f"{App.current_selected_child_name} logged in")

    def logout_child(self):
        db.connect()
        db.add_logout_time(App.current_selected_child_id, datetime.now())
        #update the notify circle where the child name
        for i, name in enumerate(App.childrens):
            if name[1] == App.current_selected_child_name:
                self.notify_circles[i].configure(bg_color="red")
        db.close()
        self.add_note(f"{App.current_selected_child_name} logged out")

    def childrens_selector(self, child_id, child_name):
        App.current_selected_child_id = child_id
        App.current_selected_child_name = child_name
        db.connect()
        App.current_selected_child_division = db.get_division(child_id)
        db.close()
        self.childrens_label.configure(text=child_name+" - "+App.current_selected_child_division)
        self.update_notes()

    def login_selector(self):
        App.frames["Main"].pack_forget()
        self.geometry(f"{500}x{580}")
        # close the size of the window it
        self.resizable(False, False)
        self.title("Login Parents Client")
        App.frames["Login"].pack(in_=self.main_container, side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)

    def main_selector(self):
        App.frames["Login"].pack_forget()
        self.geometry(f"{1200}x{580}")
        self.resizable(False, False)
        self.title("Parents Client")
        App.frames["Main"].pack(in_=self.main_container, side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)

    def login(self, *args):
        App.parent_name = self.username_entry.get()
        password = self.password_entry.get()
        db.connect()
        is_valid = db.verify_login(App.parent_name, password)

        if is_valid:
            parent_id = db.get_parent_id(App.parent_name, password)
            db.close()
            self.username_entry.delete(0, tkinter.END)
            self.password_entry.delete(0, tkinter.END)
            self.update_data(parent_id)
            self.main_selector()
        else:
            db.close()
            if len(App.parent_name) < 3 or len(App.parent_name) > 20:
                self.username_entry.configure(border_color="red")
                self.username_entry.delete(0, tkinter.END)

            self.password_entry.configure(border_color="red")
            self.password_entry.delete(0, tkinter.END)
            
            self.error_label.configure(text="Login failed either password or username is incorrect")

    def update_data(self, parent_id: int):
        db.connect()
        # remove any previous buttons
        for button in self.childrens_buttons:
            button.destroy()

        for circle in self.notify_circles:
            circle.destroy()

        self.childrens_buttons = []
        self.notify_circles = []
        App.parent_id = parent_id

        App.childrens = db.get_childrens(parent_id)

        for i, child in enumerate(App.childrens):
            child_id = child[0]
            child_name = child[1]
            is_child_logged_in = db.is_child_logged_in(child_id)
            func_with_args = partial(self.childrens_selector, child_id, child_name)
            self.childrens_buttons.append(customtkinter.CTkButton(App.frames['Main'], text=child[1], command=func_with_args))
            self.childrens_buttons[i].place(relx=0.01, rely=0.1 + i*0.1, anchor=tkinter.NW)

            if is_child_logged_in:
                self.notify_circles.append(customtkinter.CTkLabel(App.frames['Main'], text=" ", bg_color="green", width=20, height=20))
                self.notify_circles[i].place(relx=0.16, rely=0.105 + i*0.1, anchor=tkinter.NE)
            else:
                self.notify_circles.append(customtkinter.CTkLabel(App.frames['Main'], text=" ", bg_color="red", width=20, height=20))
                self.notify_circles[i].place(relx=0.16, rely=0.105 + i*0.1, anchor=tkinter.NE)
        db.close()

        self.parent_name_label.configure(text=App.parent_name)
        self.childrens_selector(App.childrens[0][0], App.childrens[0][1])

if __name__ == "__main__":
    app = App()
    app.mainloop()