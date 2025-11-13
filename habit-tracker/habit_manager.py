import json
import os

class HabitManager:
    def __init__(self):
        self.data_file = "habits.json"
        self.habits = self.load_habits()
        self.next_id = max([h['id'] for h in self.habits] or [0]) + 1
    
    def load_habits(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_habits(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.habits, f)
    
    def add_habit(self, name):
        habit = {
            'id': self.next_id,
            'name': name,
            'completed': False
        }
        self.habits.append(habit)
        self.next_id += 1
        self.save_habits()
    
    def toggle_habit(self, habit_id):
        for habit in self.habits:
            if habit['id'] == habit_id:
                habit['completed'] = not habit['completed']
                break
        self.save_habits()
    
    def delete_habit(self, habit_id):
        self.habits = [h for h in self.habits if h['id'] != habit_id]
        self.save_habits()
    
    def get_habits(self):
        return self.habits