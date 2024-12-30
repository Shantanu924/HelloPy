import random
import tkinter as tk

words = ["Stapler", "Desk", "Pay cheque", "Work computer", "Fax machine", "Phone", "Paper",
    "Light", "Chair", "Desk lamp", "Notepad", "Paper clips", "Binder", "Calculator",
    "Calendar", "Sticky Notes", "Pens", "Pencils", "Notebook", "Book", "Chairs",
    "Coffee cup", "Coffee mug", "Thermos", "Hot cup", "Glue", "Clipboard", "Paperclips",
    "Chocolate", "Secretary", "Work", "Paperwork", "Workload", "Employee", "Boredom",
    "Coffee", "Golf", "Laptop", "Sandcastle", "Monday", "Vanilla", "Bamboo", "Sneeze",
    "Scratch", "Celery", "Hammer", "Frog", "Tennis", "Hot dog", "Pants", "Bridge",
    "Bubblegum", "Candy bar", "Bucket", "Skiing", "Sledding", "Snowboarding", "Snowman",
    "Polar bear", "Cream", "Waffle", "Pancakes", "Ice cream", "Sundae", "Beach",
    "Sunglasses", "Surfboard", "Watermelon", "Baseball", "Bat", "Ball", "T-shirt", "Kiss",
    "Jellyfish", "Jelly", "Butterfly", "Spider", "Broom", "Spiderweb", "Mummy", "Candy",
    "Bays", "Squirrels", "Basketball", "Water Bottle", "Unicorn", "Dog leash", "Newspaper",
    "Hammock", "Video camera", "Money", "Smiley face", "Umbrella", "Picnic basket",
    "Teddy bear", "Ambulance", "Ancient Pyramids", "Bacteria", "Goosebumps", "Pizza",
    "Platypus", "Clam Chowder", "Goldfish bowl", "Skull", "Spiderweb", "Smoke", "Tree",
    "Ice", "Blanket", "Seaweed", "Flame", "Bubble", "Hair", "Tooth", "Leaf", "Worm", "Sky",
    "Apple", "Plane", "Cow", "House", "Dog", "Car", "Bed", "Furniture", "Train", "Rainbow",
    "Paintings", "Drawing", "Cup", "Plate", "Bowl", "Cushion", "Sofa", "Sheet", "Kitchen",
    "Table", "Candle", "Shirt", "Clothes", "Dress", "Pillow", "Home", "Toothpaste", "Guitar",
    "Schoolbag", "Pencil Case", "Glasses", "Towel", "Watch", "Piano", "Pen", "Hat", "Shoes",
    "Socks", "Jeans", "Hair Gel", "Keyboard", "Jacket", "Tie", "Bandage", "Scarf", "Hair Brush",
    "Cell Phone"]


def new_game():
    global word, scrambled_word
    word = random.choice(words)
    scrambled_word = ''.join(random.sample(word, len(word)))
    scrambled_label.config(text=f"Unscramble word: {scrambled_word}")
    result_label.config(text="")
    guess_entry.delete(0, tk.END)

def check_guess():
    guess = guess_entry.get().strip()
    if guess == word:
        result_label.config(text="Correct!", fg="green")
    else:
        result_label.config(text=f"Wrong! The word was {word}", fg="red")

root = tk.Tk()
root.title("Word Scramble Game")

scrambled_label = tk.Label(root, text="", font=("monospace", 20))
scrambled_label.pack(pady=20)

guess_entry = tk.Entry(root, font=("monospace", 16), width=30)
guess_entry.pack(pady=10)

submit_btn = tk.Button(root, text="Check", font=("monospace", 16), command=check_guess)
submit_btn.pack(pady=10)

new_game_btn = tk.Button(root, text="New Game", font=("monospace", 16), command=new_game)
new_game_btn.pack(pady=10)

result_label = tk.Label(root, text="", font=("monospace", 16))
result_label.pack(pady=10)
new_game()

root.mainloop()