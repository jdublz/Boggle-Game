import os
import random
import tkinter as tk
from tkinter import messagebox
import sys

# Get the path to the folder where the executable is located
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Load a dictionary of valid words (in uppercase) from the words.txt file
words_file_path = os.path.join(base_path, "words.txt")
with open(words_file_path, "r") as f:
    valid_words = set(word.strip().upper() for word in f)

# Constants
GRID_SIZE = 4
CELL_SIZE = 100
BOGGLE_DICE = [
    "AACIOT", "ABILTY", "ABJMOQ", "ACDEMP",
    "ACELRS", "ADENVZ", "AHMORS", "BIFORX",
    "DENOSW", "DKNOTU", "EEFHIY", "EGKLUY",
    "EGINTV", "EHINPS", "ELPSTU", "GILRUW"
]
GRID_BACKGROUND_COLOR = "#f5deb3"
used_words = set()
score = 0
game_running = False
time_left = 60

# Helper function to create the Boggle grid
def create_boggle_grid():
    random.shuffle(BOGGLE_DICE)
    return [[random.choice(BOGGLE_DICE[i * GRID_SIZE + j]) for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

# Depth-first search to check if a word can be formed on the grid
def is_word_possible(grid, word, row, col, used):
    if len(word) == 0:
        return True
    if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE or used[row][col]:
        return False
    if grid[row][col] != word[0]:
        return False
    used[row][col] = True
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for drow, dcol in directions:
        if is_word_possible(grid, word[1:], row + drow, col + dcol, used):
            return True
    used[row][col] = False
    return False

def check_word_in_boggle(grid, word):
    used = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if is_word_possible(grid, word, row, col, used):
                return True
    return False

def calculate_score(word):
    length = len(word)
    if length == 3 or length == 4:
        return 1
    elif length == 5:
        return 2
    elif length == 6:
        return 3
    elif length == 7:
        return 5
    elif length >= 8:
        return 11
    return 0

def update_scoreboard(word):
    global score
    if word not in used_words:
        used_words.add(word)
        points = calculate_score(word)
        score += points
        score_label.config(text=f"Score: {score}")
        used_words_list.insert(tk.END, word)

def check_word():
    global game_running
    if not game_running:
        messagebox.showinfo("Time's Up", "The game is over. Please restart to play again.")
        return
    word = word_entry.get().upper()
    
    # Check if the word is valid in the dictionary
    if word not in valid_words:
        messagebox.showinfo("Result", f"The word '{word}' is not in the dictionary.")
        return
    
    if word in used_words:
        messagebox.showinfo("Result", f"The word '{word}' has already been used.")
    elif check_word_in_boggle(grid, word):
        update_scoreboard(word)
    else:
        messagebox.showinfo("Result", f"The word '{word}' cannot be formed from the grid.")
    
    # Clear the word entry box after checking the word
    word_entry.delete(0, tk.END)

def start_over():
    global grid, score, used_words, game_running, time_left
    grid = create_boggle_grid()
    display_grid()
    score = 0
    used_words.clear()
    used_words_list.delete(0, tk.END)
    score_label.config(text=f"Score: {score}")
    word_entry.delete(0, tk.END)
    game_running = True
    time_left = 75
    update_timer()

def display_grid():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            grid_label = tk.Label(window, text=grid[i][j], font=('Helvetica', 24), width=2, height=1, relief="solid", bd=1, bg=GRID_BACKGROUND_COLOR)
            grid_label.grid(row=i, column=j, padx=0, pady=0, sticky="nsew")
            grid_label.config(width=int(CELL_SIZE/20), height=int(CELL_SIZE/40))
    for i in range(GRID_SIZE):
        window.grid_columnconfigure(i, minsize=CELL_SIZE)
        window.grid_rowconfigure(i, minsize=CELL_SIZE)

def show_rules():
    rules_window = tk.Toplevel(window)
    rules_window.title("Boggle Rules")
    rules_window.transient(window)
    rules_window.grab_set()
    rules_window.geometry("+700+300")  # Position the rules window more to the right
    rules_text = """Boggle Rules:
1. Find words by connecting adjacent letters.
2. Words must be at least 3 letters long.
3. Letters can be connected horizontally, vertically, or diagonally.
4. You cannot reuse a letter in the same word."""
    rules_label = tk.Label(rules_window, text=rules_text, font=('Helvetica', 14), padx=10, pady=10)
    rules_label.pack()
    start_button = tk.Button(rules_window, text="Start Game", font=('Helvetica', 14), command=lambda: [rules_window.destroy(), resize_window(), start_over()])
    start_button.pack(pady=10)
    rules_window.wait_window()

def update_timer():
    global time_left, game_running
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Time Left: {time_left}s")
        window.after(1000, update_timer)
    else:
        game_running = False
        messagebox.showinfo("Time's Up", "The game is over! You can start a new game.")

def resize_window():
    window.geometry(f"{GRID_SIZE * (CELL_SIZE + 10) + 400}x{(GRID_SIZE + 8) * (CELL_SIZE // 2)}+500+100")

# Initialize the window
window = tk.Tk()
window.title("Boggle Game by Joey!")
window.geometry(f"{GRID_SIZE * (CELL_SIZE + 10) + 300}x{(GRID_SIZE + 3) * (CELL_SIZE // 2)}+500+100")

# Timer
timer_label = tk.Label(window, text=f"Time Left: {time_left}s", font=('Helvetica', 14))
timer_label.grid(row=0, column=GRID_SIZE + 1, padx=20, sticky="nw")

# Scoreboard
score_label = tk.Label(window, text=f"Score: {score}", font=('Helvetica', 14))
score_label.grid(row=1, column=GRID_SIZE + 1, padx=20, sticky="nw")

# Used words list
used_words_label = tk.Label(window, text="Used Words:", font=('Helvetica', 14))
used_words_label.grid(row=2, column=GRID_SIZE + 1, padx=20, sticky="nw")
used_words_list = tk.Listbox(window, font=('Helvetica', 14), height=10, width=20)
used_words_list.grid(row=3, column=GRID_SIZE + 1, rowspan=4, padx=20, pady=10, sticky="nw")

# Word entry and button
word_entry_label = tk.Label(window, text="Enter a word:", font=('Helvetica', 14))
word_entry_label.grid(row=GRID_SIZE, column=0, columnspan=2, pady=10)
word_entry = tk.Entry(window, font=('Helvetica', 14))
word_entry.grid(row=GRID_SIZE, column=2, columnspan=2, pady=10)

# Bind the Enter key to submit the word
window.bind('<Return>', lambda event: check_word())

# Button to check the word (optional if you'd like to keep the button as well)
check_button = tk.Button(window, text="Check Word", font=('Helvetica', 14), command=check_word)
check_button.grid(row=GRID_SIZE + 1, column=0, columnspan=4, pady=10)

# "Start Over" button
start_over_button = tk.Button(window, text="Start Over", font=('Helvetica', 14), command=start_over)
start_over_button.grid(row=GRID_SIZE + 2, column=GRID_SIZE + 1, pady=10)

# Show rules on startup
show_rules()

# Run the main loop
window.mainloop()
