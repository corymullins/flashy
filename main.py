from tkinter import *
import pandas as pd
import random

# ------------------------- CONSTANTS ---------------------
# Constants for colors and fonts
BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = "Ariel", 40, "italic"
WORD_FONT = "Ariel", 60, "bold"
LANGUAGE = ""
WORD = ""

# ----------------------- LOAD CSV DATA --------------------
# Load CSV data into 'to_learn' list of dictionaries
words_file = "./data/words_to_learn.csv"

try:
    data = pd.read_csv(words_file)
except FileNotFoundError:
    # Load original data if file not found
    original_data = pd.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# ------------------------- SHOW WORD ----------------------
# Display a word on the canvas
def show_word():
    global current_word

    # Pick random word
    current_word = random.choice(to_learn)

    # Show French word
    canvas.itemconfig(lang_text, text="French")
    canvas.itemconfig(word_text, text=current_word["French"])

    # After 3 seconds show English word
    window.after(3000, card_flip)

# -------------------------- CARD FLIP ----------------------
# Flip the flashcard to show the translation
def card_flip():
    # Show English word
    canvas.itemconfig(canvas_img, image=card_back_img)
    canvas.itemconfig(lang_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_word['English'], fill="white")

# ----------------------- WORDS TO REMOVE --------------------
# Move the current word to the known words list and update the CSV
def is_known():
    global words_file

    to_learn.remove(current_word)

    data = pd.DataFrame(to_learn)
    data.to_csv(words_file, index=False)

    show_word()

# ------------------------- UI SETUP ------------------------
# Set up the GUI window and canvas
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
canvas_img = canvas.create_image(400, 263, image=card_front_img)
lang_text = canvas.create_text(400,150, text="", fill="black", font=LANGUAGE_FONT)
canvas.grid(column=0,row=0, columnspan=2)
word_text = canvas.create_text(400,263, text="", fill="black", font=WORD_FONT)
canvas.grid(column=0,row=2, columnspan=2)

right_img = PhotoImage(file="./images/right.png")
wrong_img = PhotoImage(file="./images/wrong.png")

no_button = Button(image=wrong_img, highlightthickness=0, command=show_word)
no_button.grid(column=0,row=3)

yes_button = Button(image=right_img, highlightthickness=0, command=is_known)
yes_button.grid(column=1,row=3)

# Start by showing a word
show_word()

# Run the GUI main loop
window.mainloop()