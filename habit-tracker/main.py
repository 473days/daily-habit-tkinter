import tkinter as tk
from tkinter import messagebox, simpledialog
from habit_manager import HabitManager

class HabitTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Habit Tracker Pro")
        self.root.geometry("600x600")
        self.root.configure(bg="#f5f5f5")
        
        self.habit_manager = HabitManager()
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#4CAF50", height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Daily Habit Tracker", 
                              font=("Arial", 20, "bold"), bg="#4CAF50", fg="white")
        title_label.pack(expand=True)
        
        # Stats frame
        stats_frame = tk.Frame(self.root, bg="white", relief=tk.RAISED, bd=1)
        stats_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.stats_label = tk.Label(stats_frame, text="Total: 0 | Completed: 0", 
                                   font=("Arial", 10), bg="white")
        self.stats_label.pack(pady=5)
        
        # Add habit section
        add_frame = tk.Frame(self.root, bg="#f5f5f5")
        add_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.habit_entry = tk.Entry(add_frame, width=40, font=("Arial", 12))
        self.habit_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.habit_entry.bind("<Return>", lambda e: self.add_habit())
        
        add_button = tk.Button(add_frame, text="Add Habit", 
                              command=self.add_habit, bg="#2196F3", fg="white",
                              font=("Arial", 10, "bold"))
        add_button.pack(side=tk.RIGHT, padx=5)
        
        # Habits list with scrollbar
        list_frame = tk.Frame(self.root, bg="#f5f5f5")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create scrollable canvas
        self.canvas = tk.Canvas(list_frame, bg="white", relief=tk.SUNKEN, bd=1)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        self.refresh_habits()
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def add_habit(self):
        habit_text = self.habit_entry.get().strip()
        if habit_text:
            self.habit_manager.add_habit(habit_text)
            self.habit_entry.delete(0, tk.END)
            self.refresh_habits()
        else:
            messagebox.showwarning("Warning", "Please enter a habit name")
    
    def toggle_habit(self, habit_id):
        self.habit_manager.toggle_habit(habit_id)
        self.refresh_habits()
    
    def delete_habit(self, habit_id):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this habit?"):
            self.habit_manager.delete_habit(habit_id)
            self.refresh_habits()
    
    def edit_habit(self, habit_id, old_name):
        new_name = simpledialog.askstring("Edit Habit", "Enter new habit name:", 
                                           initialvalue=old_name)
        if new_name and new_name.strip():
            self.habit_manager.update_habit_name(habit_id, new_name.strip())
            self.refresh_habits()
    
    def refresh_habits(self):
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        habits = self.habit_manager.get_habits()
        
        # Update stats
        total = len(habits)
        completed = sum(1 for habit in habits if habit['completed'])
        self.stats_label.config(text=f"Total: {total} | Completed: {completed} | Progress: {completed}/{total}")
        
        # Create habit widgets
        for habit in habits:
            self.create_habit_widget(habit)
            
        # Show message if no habits
        if not habits:
            empty_label = tk.Label(self.scrollable_frame, text="No habits yet. Add one above!",
                                  font=("Arial", 12), fg="gray", bg="white")
            empty_label.pack(pady=50)
    
    def create_habit_widget(self, habit):
        habit_frame = tk.Frame(self.scrollable_frame, bg="white", relief=tk.RAISED, bd=1)
        habit_frame.pack(fill=tk.X, pady=2, padx=5)
        
        # Checkbox
        check_var = tk.BooleanVar(value=habit['completed'])
        check_button = tk.Checkbutton(
            habit_frame,
            variable=check_var,
            command=lambda id=habit['id']: self.toggle_habit(id),
            bg="white"
        )
        check_button.pack(side=tk.LEFT, padx=5)
        
        # Habit name with styling - this will expand to fill available space
        if habit['completed']:
            name_label = tk.Label(habit_frame, text=habit['name'], 
                                 fg="green", font=("Arial", 11, "overstrike"),
                                 bg="white", anchor="w")
        else:
            name_label = tk.Label(habit_frame, text=habit['name'], 
                                 font=("Arial", 11), bg="white", anchor="w")
        
        name_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Button frame to hold edit and delete buttons
        button_frame = tk.Frame(habit_frame, bg="white")
        button_frame.pack(side=tk.RIGHT, padx=5)
        
        # Edit button
        edit_btn = tk.Button(button_frame, text="Edit", font=("Arial", 9),
                           command=lambda id=habit['id'], name=habit['name']: self.edit_habit(id, name),
                           bg="#FFC107", relief=tk.FLAT, width=4)
        edit_btn.pack(side=tk.LEFT, padx=2)
        
        # Delete button
        delete_btn = tk.Button(button_frame, text="Delete", font=("Arial", 9),
                             command=lambda id=habit['id']: self.delete_habit(id),
                             bg="#F44336", fg="white", relief=tk.FLAT, width=4)
        delete_btn.pack(side=tk.LEFT, padx=2)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = HabitTracker()
    app.run()
