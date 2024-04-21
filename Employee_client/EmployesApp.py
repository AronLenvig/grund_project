import tkinter as tk
import customtkinter as ctk
import os
from Employee_client.EmployeeMainBody import EmployeeMainBody

ctk.set_appearance_mode("system")  # Modes: system (default), light, dark
ctk.set_default_color_theme("dark-blue") # Themes: blue (default), dark-blue, green
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        #window settings
        self.title("Employee Client")
        self.geometry(f"{1200}x{600}")
        self.resizable(False, False)

        #main frame where all the other frames are placed
        self.main_header = ctk.CTkFrame(self)
        self.main_header.pack(fill=tk.BOTH, expand=True)
        self.main_header.grid_columnconfigure(0, weight=1)

        #label kinder garden on the top left
        self.main_title = ctk.CTkLabel(self.main_header, text="Midtbyens Naturbørnehus", font=("Arial", 34, "bold"))
        self.main_title.grid(row=0, column=0, sticky="ew")

        #main_body under the main frame
        self.main_body = EmployeeMainBody(self.main_header, height=500)
        self.main_body.grid(row=2, column=0, sticky="ew")

        #three SegmentedButton for choosing the division
        self.division_buttons = ctk.CTkSegmentedButton(self.main_header, values=["Nature", "Technology", "Humanity"], width=300, command=self.main_body.change_division)
        self.division_buttons.grid(row=1, column=0, sticky="ew")
        #preselect the first button
        self.division_buttons.set("Nature")
        self.fixed_update()

    def fixed_update(self):
        self.main_body.refresh()
        self.after(1000, self.fixed_update)

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()