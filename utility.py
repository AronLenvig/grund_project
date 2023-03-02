import tkinter.messagebox
import tkinter as tk
from datetime import datetime, timedelta
import customtkinter as ctk

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def verify_dialog(dilog):
    if not dilog:
        return False
    
    if len(dilog) > 100:
        tkinter.messagebox.showerror("Error", "Note must be less than 100 characters")
        return False

    return True

def find_value_in_day(selected_day: int, time_in_week: list[tuple[datetime, datetime]]):
        result = []
        for day in time_in_week:
            if day[0].weekday() == selected_day:
                result.append(day)
        return result
    
def calculate_time_in_day(time_in_day: list[tuple[datetime, datetime]]):
    total_time = timedelta()
    for day in time_in_day:
        if day[1] == None:
            total_time += datetime.now() - day[0]
        else:
            total_time += day[1] - day[0]
    return total_time

def create_dialog(text, title):
    dialog = ctk.CTkInputDialog(text=text, title=title)
    text = dialog.get_input()
    return text

def get_week_days():
    return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def verify_password(new_password):
        if not new_password:
            return False

        if len(new_password) < 6:
            tk.messagebox.showerror("Error", "Password must be more than 6 characters")
            return False
        if len(new_password) > 20:
            tk.messagebox.showerror("Error", "Password must be less than 20 characters")
            return False
        
        tk.messagebox.showinfo("Success", "Password changed successfully")
        return True
