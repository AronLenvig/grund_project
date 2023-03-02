import tkinter as tk
import customtkinter as ctk
import data.db_context as db
from datetime import datetime, timedelta
import utility as util


class NotesFrame(ctk.CTkFrame):
    def __init__(self, app, width=400, height=400, admin=False):
        super().__init__(app, width=width, height=height)
        self.app = app
        self.notes_date = 0
        self.notes = []
        self.admin = admin
        self._height = height


        self.grid_columnconfigure(0, weight=1)
        self.title_label = ctk.CTkLabel(self, text="current day", font=("Arial", 20, "bold"))
        self.title_label.grid( row=0, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="ew")

        self.previous_day_button = ctk.CTkButton(self, text="<", width=100, command=lambda: self.update_date(-1))
        self.previous_day_button.grid(row=1, column=0, padx=10, pady=(3, 3), sticky="ew")

        self.next_day_button = ctk.CTkButton(self, text=">", width=100, command=lambda: self.update_date(1))
        self.next_day_button.grid(row=1, column=1, padx=10, pady=(3, 3), sticky="ew")

        self.add_note_button = ctk.CTkButton(self, text="Add note", command=self.add_note)
        self.add_note_button.grid(row=2, column=0, columnspan=2, padx=10, pady=(3, 3), sticky="ew")

        self.note_row = 3
        if self.admin:
            self.note_row = 4
            self.add_division_note_button = ctk.CTkButton(self, text="Add division note", command=self.add_division_note)
            self.add_division_note_button.grid(row=3, column=0, padx=10, pady=(3, 3), sticky="ew")

            self.add_company_note_button = ctk.CTkButton(self, text="Add company note", command=self.add_company_note)
            self.add_company_note_button.grid(row=3, column=1, padx=10, pady=(3, 3), sticky="ew")
            pass
        
        self.notes_text = ctk.CTkTextbox(self, height=300, state=tk.DISABLED)
        self.notes_text.grid(row=self.note_row, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="ew")

    def update_date(self, amount):
        self.notes_date += amount
        self.update_notes()

    def add_note(self, note: str = None):
        is_staff = self.admin
        if not note:
            dilog = util.create_dialog("add a note", "Note")
            if not util.verify_dialog(dilog):
                return
            note = dilog
        db.connect()
        db.add_note_to_child(self.app.current_selected_child_id, note, is_staff)
        db.close()
        self.update_notes()

    def add_division_note(self):
        dilog = util.create_dialog("add a note for divison", "Note(company)")
        if not util.verify_dialog(dilog):
            return
        db.connect()
        db.add_note_to_division(self.app.current_selected_child_division, dilog)
        db.close()
        self.update_notes()
        
    def add_company_note(self):
        dilog = util.create_dialog("add a note for company", "Note(divison)")
        if not util.verify_dialog(dilog):
            return
        db.connect()
        db.add_note_to_company(dilog)
        db.close()
        self.update_notes()
    
    def update_notes(self):
        db.connect()
        notes = db.get_notes_day(self.app.current_selected_child_id, self.notes_date)
        div_notes = db.get_divison_notes_day(self.app.current_selected_child_division, self.notes_date)
        company_notes = db.get_company_notes_day(self.notes_date)
        db.close()
        self.notes_text.configure(state=tk.NORMAL)
        self.notes_text.delete(1.0, tk.END)
        parent_notes = [note for note in notes if not note[2]]
        staff_notes = [note for note in notes if note[2]]

        self.create_note_format("red", company_notes, 0)
        self.create_note_format("orange", div_notes, len(company_notes))
        self.create_note_format("green", parent_notes, len(company_notes) + len(div_notes))
        if self.app.app._get_appearance_mode() == "dark":
            self.create_note_format("cyan", staff_notes, len(company_notes) + len(div_notes) + len(parent_notes))
        else:
            self.create_note_format("blue", staff_notes, len(company_notes) + len(div_notes) + len(parent_notes))

        self.notes_text.configure(state=tk.DISABLED)

        # current day minus/plus notes date = the day
        curenntly_selected_day = (datetime.now() + timedelta(days=self.notes_date)).strftime("%d/%m")
        self.title_label.configure(text="Notes - "+ curenntly_selected_day)

    def create_note_format(self, color: str, notes: list[tuple[datetime, str]], start_index: int):
        for i, note in enumerate(notes[::-1]):
            i += start_index
            note_text = ""
            note_text += note[0].strftime("%H:%M:%S") + " - "
            note_text += note[1]
            note_text += "\n"
            self.notes_text.insert(tk.END, note_text)
            self.notes_text.tag_add(color, f"{i+1}.0", f"{i+1}.end")
            self.notes_text.tag_config(color, foreground=color)
    

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesFrame(root, 800, 600)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()