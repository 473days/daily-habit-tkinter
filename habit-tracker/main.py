import tkinter as tk
from habit_manager import HabitManager

class HabitTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Daily Habit Tracker")
        self.root.geometry("400x500")
        
        self.habit_manager = HabitManager()
        self.setup_ui()
        
    def setup_ui(self):
        title_label = tk.Label(self.root, text="My Daily Habits", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        self.habit_entry = tk.Entry(self.root, width=30)
        self.habit_entry.pack(pady=5)
        
        add_button = tk.Button(self.root, text="Add Habit", command=self.add_habit)
        add_button.pack(pady=5)
        
        self.habits_frame = tk.Frame(self.root)
        self.habits_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.refresh_habits()
        
    def add_habit(self):
        habit_text = self.habit_entry.get().strip()
        if habit_text:
            self.habit_manager.add_habit(habit_text)
            self.habit_entry.delete(0, tk.END)
            self.refresh_habits()
    
    def toggle_habit(self, habit_id):
        # Use the existing toggle_habit method from habit_manager
        self.habit_manager.toggle_habit(habit_id)
        self.refresh_habits()
    
    def delete_habit(self, habit_id):
        self.habit_manager.delete_habit(habit_id)
        self.refresh_habits()
    
    def refresh_habits(self):
        for widget in self.habits_frame.winfo_children():
            widget.destroy()
        
        habits = self.habit_manager.get_habits()
        for habit in habits:
            self.create_habit_widget(habit)
    
    def create_habit_widget(self, habit):
        habit_frame = tk.Frame(self.habits_frame, relief=tk.RAISED, bd=1)
        habit_frame.pack(fill=tk.X, pady=2)
        
        # Create checkbox - no need for BooleanVar since we're toggling directly
        check_button = tk.Checkbutton(
            habit_frame,
            command=lambda id=habit['id']: self.toggle_habit(id)
        )
        check_button.pack(side=tk.LEFT, padx=5)
        
        # Set the initial state of the checkbox
        if habit['completed']:
            check_button.select()
        
        # Style the label based on completion status
        label_text = habit['name']
        if habit['completed']:
            label = tk.Label(habit_frame, text=label_text, fg="green", font=("Arial", 10, "overstrike"))
        else:
            label = tk.Label(habit_frame, text=label_text)
        
        label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        delete_btn = tk.Button(habit_frame, text="X", 
                              command=lambda id=habit['id']: self.delete_habit(id))
        delete_btn.pack(side=tk.RIGHT, padx=5)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = HabitTracker()
    app.run()