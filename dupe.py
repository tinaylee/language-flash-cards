from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_word = {}
timer = 0

try:
    spanish_words = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    spanish_words = pandas.read_csv("./data/spanish_words.csv")
finally:
    spanish_dict = spanish_words.to_dict(orient="records")


def new_word():
    global current_word, timer
    window.after_cancel(timer)
    reset()
    canvas.itemconfig(flashcard, image=card_front)
    current_word = random.choice(spanish_dict)
    canvas.itemconfig(language_text, text="Spanish")
    canvas.itemconfig(word_text, text=current_word['Spanish'])
    timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(flashcard, image=card_back)
    show_answer()


def show_answer():
    canvas.itemconfig(word_text, text=current_word['English'])
    canvas.itemconfig(language_text, fill="white")
    canvas.itemconfig(word_text, fill="white")

def reset():
    canvas.itemconfig(word_text, fill="black")
    canvas.itemconfig(language_text, fill="black")

def correct_answer():
    spanish_dict.remove(current_word)
    df = pandas.DataFrame(spanish_dict)
    df.to_csv("./data/words_to_learn.csv", index=False)
    new_word()


window = Tk()
window.title("Flashcards - 2nd Try")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
flashcard = canvas.create_image(400, 263, image=card_front)
language_text = canvas.create_text(400, 150, text="language", font=('Arial', 40, 'italic'))
word_text = canvas.create_text(400, 263, text="word", font=('Arial', 60, 'bold'))

canvas.grid(row=0, column=0, columnspan=2)

checkmark = PhotoImage(file="./images/right.png")
x = PhotoImage(file="./images/wrong.png")
correct_button = Button(image=checkmark, highlightthickness=0, bd=0, command=correct_answer)
correct_button.grid(row=1, column=0)
wrong_button = Button(image=x, highlightthickness=0, bd=0, command=new_word)
wrong_button.grid(row=1, column=1)

timer = window.after(3000, flip_card)
new_word()

window.mainloop()