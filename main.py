from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
timer = 0
current_card = {}

# ---------------------------------Data Import---------------------------------
try:
    spanish_words = pandas.read_csv("./data/words_to_learn_main.csv")
except FileNotFoundError:
    spanish_words = pandas.read_csv("./data/spanish_words.csv")
# Convert to dictionary
finally:
    spanish_dict = spanish_words.to_dict(orient="records")


# ---------------------------------FUNCTIONS---------------------------------
def random_word():
    global current_card, timer
    window.after_cancel(timer)
    reset_card()
    current_card = random.choice(spanish_dict)
    canvas.itemconfig(word_text, text=current_card['Spanish'])
    canvas.itemconfig(language_text, text="Spanish")
    timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back)
    translate()


def reset_card():
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(word_text, fill="black")
    canvas.itemconfig(language_text, fill="black")


def translate():
    canvas.itemconfig(word_text, text=current_card['English'], fill="white")
    canvas.itemconfig(language_text, text="English", fill="white")


def remove_word():
    spanish_dict.remove(current_card)
    spanish_df = pandas.DataFrame(spanish_dict)
    spanish_df.to_csv("./data/words_to_learn_main.csv", index=False)


def correct_answer():
    remove_word()
    random_word()


window = Tk()
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
window.title("Flashcards")


# ---------------------------------Card UI---------------------------------
canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front, tag="current_image")
canvas.grid(row=0, column=0, columnspan=2)
language_text = canvas.create_text(400, 150, text="", font=('Arial', 40, 'italic'))
word_text = canvas.create_text(400, 263, text="", font=('Arial', 60, 'bold'))

# ---------------------------------Button UI---------------------------------

checkmark = PhotoImage(file="./images/right.png")
right_button = Button(image=checkmark, highlightthickness=0, bd=0, highlightbackground=BACKGROUND_COLOR,
                      command=correct_answer)
right_button.grid(row=1, column=0, pady=50)

x = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=x, highlightthickness=0, bd=0, highlightbackground=BACKGROUND_COLOR, command=random_word)
wrong_button.grid(row=1, column=1, pady=50)

timer = window.after(3000, flip_card)
random_word()


window.mainloop()
