import tkinter as tk
from tkinter import messagebox as msg
import sqlite3 as sql
import random
import time

texts = [
    "The quick brown fox jumped over the lazy dog.",
    "Typing is an essential skill in the digital world." ,
    "Practise makes perfect when it comes to typing speed." ,
    "A journey of thousand miles begins with a single step." ,
    "To be, or not to be, that is the question.",
    "In the heart of the bustling city, amidst the cacophony of car horns and chatter, a quiet park offered solace. The old oak tree in the center stood as a sentinel, its sprawling branches providing shade to those seeking respite. Children played on the swings, their laughter echoing in the air, while an artist sat on a bench, sketching the scene with careful strokes. It was a pocket of calm in a world that never seemed to stop moving.",
    "The vast expanse of the desert stretched endlessly, golden dunes shimmering under the blazing sun. A lone traveler trudged forward, their shadow the only companion on this solitary journey. Each step sank into the sand, leaving a fleeting imprint before the wind erased it. Despite the arid heat, the promise of an oasis kept hope alive, a mirage of water and palm trees dancing on the horizon.",
    "Technology has transformed the way we live, connecting people across continents and revolutionizing industries. The advent of the internet brought a digital era where information is at our fingertips. From smartphones to smart homes, every innovation aims to make life more convenient. However, amidst this progress, it is crucial to strike a balance, ensuring that human connections and environmental sustainability are not lost in the race for advancement.", "The forest was alive with the sounds of nature, a symphony of rustling leaves, chirping birds, and the occasional rustle of a deer moving through the underbrush. Sunlight filtered through the canopy, creating a mosaic of light and shadow on the forest floor. Every step revealed something new—a vibrant mushroom, a squirrel darting up a tree, or a cluster of wildflowers swaying in the gentle breeze.","Traveling to a new place is like opening the pages of an unfamiliar book. Every street, every corner holds a story waiting to be discovered. From the aroma of local cuisine wafting through the air to the vibrant colors of a bustling market, each moment is a feast for the senses. It is not just about the destination but the journey, the people you meet, and the memories you create along the way."
]

conn = sql.connect("typing_master.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
username TEXT PRIMARY KEY,
password TEXT,
best_wpm INTEGER
)
""")
conn.commit()

class TypingMasterApp:
    def __init__(self,root):
        self.root = root
        self.root.title("Typing Master App")
        self.username = None
        self.start_time = None
        self.selected_text = ""
        self.login_screen()
    
    def login_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Welcome to typing master...", font=("Monospace",18)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack()

        tk.Label(self.root, text="Password").pack()
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.register).pack()
    
    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if not username or not password:
            msg.showerror("Error","Please fill all fields")
            return
        
        cursor.execute("SELECT* FROM users WHERE username = ?",(username,))
        if cursor.fetchone():
            msg.showerror("Error","User already exists")
        else:
            cursor.execute("INSERT INTO users(username, password, best_wpm) VALUES(?,?,?)",(username,password,0))
            conn.commit()
            msg.showinfo("Success","Registered Successfully! Please Login.")
    
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",(username,password))
        user = cursor.fetchone()
        if user:
            self.username = username
            self.main_screen()
        else:
            msg.showerror("Error","Invalid username or password")
    
    def main_screen(self):
        self.clear_frame()

        tk.Label(self.root, text=f"Welcome, {self.username}!", font=("Monospace",18)).pack(pady=10)
        tk.Button(self.root, text="Start Typing Practice", command=self.start_typing_practice).pack(pady=5)
        tk.Button(self.root, text="View Best WPM", command = self.view_best_wpm).pack(pady=5)
        tk.Button(self.root, text="Logout", command = self.logout).pack(pady=5)
    
    def start_typing_practice(self):
        self.clear_frame()
        self.selected_text = random.choice(texts)
        self.start_time = time.time()

        tk.Label(self.root,text="Type the text below:", font=("Monospace",14)).pack(pady=10)
        tk.Label(self.root,text=self.selected_text, wraplength=400, justify="center",font=("Monospace",12)).pack(pady=10)

        self.typing_area = tk.Text(self.root, height = 5, wrap="word")
        self.typing_area.pack(pady=10)

        tk.Button(self.root,text="Submit", command=self.calculate_wpm).pack(pady=5)
    
    def calculate_wpm(self):
        end_time = time.time()
        typed_text = self.typing_area.get("1.0","end-1c")
        words_typed = len(typed_text.split())
        elapsed_time = (end_time - self.start_time)/60
        wpm = int(words_typed/elapsed_time)

        if typed_text.strip() == self.selected_text.strip():
            msg.showinfo("Typing Speed", f"Well done! your typing speed is {wpm} WPM.")
            cursor.execute("SELECT best_wpm FROM users WHERE username = ?", (self.username,))
            best_wpm = cursor.fetchone()[0]
            if wpm > best_wpm:
                cursor.execute("UPDATE users SET best_wpm = ? WHERE username = ?", (wpm,self.username))
                conn.commit()
                msg.showinfo("New Record", f"Congratulations! you set a new record of {wpm} WPM.")
        else:
            msg.showerror("Error","Text does not match! Try again.")

        self.main_screen()
    
    def view_best_wpm(self):
        cursor.execute("SELECT best_wpm FROM users WHERE username = ?",(self.username,))
        best_wpm = cursor.fetchone()[0]
        msg.showinfo("Best WPM", f"Your best WPM is {best_wpm}.")
    
    def logout(self):
        self.username = None
        self.login_screen()
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

root = tk.Tk()
app = TypingMasterApp(root)
root.mainloop()

conn.close()
