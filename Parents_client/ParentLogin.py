import customtkinter as ctk
import tkinter as tk
import data.db_context as db



#class login
class ParentLogin(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app)

        self.app = app

        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=0)

        self.username_label = ctk.CTkLabel(self, text="Username")
        self.username_label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

        self.username_entry = ctk.CTkEntry(self, width=200)
        self.username_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.password_label = ctk.CTkLabel(self, text="Password")
        self.password_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.password_entry = ctk.CTkEntry(self, width=200, show="*")
        self.password_entry.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.error_label = ctk.CTkLabel(self, text="",)
        self.error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        self.username_entry.bind("<Return>", self.login)
        self.password_entry.bind("<Return>", self.login)
        self.username_entry.bind("<FocusIn>", lambda event: self.username_entry.configure(border_color="grey"))
        self.password_entry.bind("<FocusIn>", lambda event: self.password_entry.configure(border_color="grey"))
        self.username_entry.bind("<Button-1>", lambda event: self.username_entry.configure(border_color="grey"))
        self.password_entry.bind("<Button-1>", lambda event: self.password_entry.configure(border_color="grey"))

    def login(self, *args):
        parent = self.username_entry.get()
        self.app.parent_client.parent_name = parent
        password = self.password_entry.get()
        db.connect()
        is_valid = db.verify_login(parent, password)

        if is_valid:
            self.error_label.configure(text="")
            parent_id = db.get_parent_id(parent, password)
            db.close()
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.app.parent_client.children_selector.update_children_view_from_selected_parents(parent_id)
            self.app.main_selector()
            self.app.parent_client.fixed_update()
        else:
            db.close()
            if len(parent) < 3 or len(parent) > 20:
                self.username_entry.configure(border_color="red")
                self.username_entry.delete(0, tk.END)

            self.password_entry.configure(border_color="red")
            self.password_entry.delete(0, tk.END)
            
            self.error_label.configure(text="Login failed either password or username is incorrect")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f"{500}x{580}")
    root.resizable(False, False)
    root.title("Login Parents Client")
    app = ParentLogin(root)
    app.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()

