import tkinter as tk
import customtkinter as ctk
import data.db_context as db
from datetime import datetime, timedelta
import utility as util

class OverviewFrame(ctk.CTkFrame):
    def __init__(self, app, width=400, height=400):
        super().__init__(app, width=width, height=height)
        self.app = app
        self.time_in_week = 0
        self.progressbars = []
        self.progressbar_labels = []

        self.grid_columnconfigure(0, weight=1)
        self.title_label = ctk.CTkLabel(self, text="Week 2: (07/01-14/02)", font=("Arial", 20, "bold"))
        self.title_label.grid( row=0, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="ew")
        self.previous_week_button = ctk.CTkButton(self, text="<", width=100, command=lambda: self.update_week(-1))
        self.previous_week_button.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="ew")
        self.next_week_button = ctk.CTkButton(self, text=">", width=100, command=lambda: self.update_week(1))
        self.next_week_button.grid(row=1, column=1, padx=10, pady=(10, 10), sticky="ew")

        for i, day in enumerate(util.get_week_days()):
            i += 2
            #create a progressbar for each day
            self.progressbar_label = ctk.CTkLabel(self, text=day)
            self.progressbar_label.grid(row=i*2-1, column=0, padx=10, columnspan=2, pady=(0, 3), sticky="ew")
            self.progressbar_labels.append(self.progressbar_label)
            self.progressbar = ctk.CTkProgressBar(self, width=200, mode="determinate")
            self.progressbar.grid(row=i*2, column=0, padx=10, columnspan=2, pady=(0, 10), sticky="ew")
            self.progressbars.append(self.progressbar)

    def update_week(self, week: int):
        self.time_in_week += week
        self.update_overview()
    
    def update_overview(self):
        # get the data from the database for current selected child
        db.connect()
        week_data = db.get_login_time_in_week(self.app.current_selected_child_id, self.time_in_week)
        db.close()
        current_week = datetime.now().isocalendar()[1] + self.time_in_week
        if current_week > 52:
            current_week = 1
        if current_week < 1:
            current_week = 52

        #get the first day of current_week and last day of current_week in format: day/month
        first_day = (datetime.strptime(f"{current_week}-1", "%W-%w") + timedelta(days=1)).strftime("%d/%m")
        last_day = (datetime.strptime(f"{current_week}-1", "%W-%w") + timedelta(days=7)).strftime("%d/%m")
        
        if len(str(current_week)) == 1:
            current_week = "0" + str(current_week)

        self.title_label.configure(text=f"Week {current_week} - ({first_day} - {last_day})")

        for i, day in enumerate(util.get_week_days()):
            time_in_day = util.calculate_time_in_day(util.find_value_in_day(i, week_data))
            # convert time_in_day seconds to hours:minutes:seconds
            hours_minutes_seconds = str(timedelta(seconds=time_in_day.seconds)) 
            self.progressbar_labels[i].configure(text=day + " - " + str(hours_minutes_seconds))
            self.progressbars[i].set((time_in_day.seconds/28800))


if __name__ == "__main__":
    root = tk.Tk()
    app = OverviewFrame(root, 800, 600)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()