from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from pathlib import Path
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_LABEL = ('Arial', 40, 'italic')
FONT_WORD = ('Arial', 60, 'bold')
MAIN_CSV = 'data/all_words.csv'
WORDS_TO_LEARN_CSV = 'data/words_to_learn.csv'

WINDOW_PADDING = 50
FLASH_WIDTH = 800
FLASH_HEIGHT = 526
LABEL_POS = (400, 150)
WORD_POS = (400, 263)

def right_action(words, canvas, window):
    words.remove(canvas.actual_word)
    save_words_to_csv(words)
    next_card(words, canvas, window)

def save_words_to_csv(words):
    df_words = pandas.DataFrame(words)
    df_words.to_csv(WORDS_TO_LEARN_CSV, index=False)

def next_card(words, canvas, window):
    canvas.actual_word = random.choice(words)
    
    if hasattr(canvas, "flip_after_id") and canvas.flip_after_id:
        window.after_cancel(canvas.flip_after_id)

    canvas.itemconfig(canvas.card_bg_img, image=canvas.front_img)
    canvas.itemconfig(canvas.label_text, text="ENGLISH", fill="black")
    canvas.itemconfig(canvas.word_text, text=canvas.actual_word["en"], fill="black")

    canvas.flip_after_id = window.after(
        3000,
        lambda: flip_card(canvas)
    )
    
    return canvas.actual_word

def flip_card(canvas):
    canvas.itemconfig(canvas.card_bg_img, image=canvas.back_img)
    canvas.itemconfig(canvas.label_text, text="POLISH", fill="white")
    canvas.itemconfig(canvas.word_text, text=canvas.actual_word["pl"], fill="white")
    
def init_UI(words, window):       
    canvas = Canvas(height=FLASH_HEIGHT, width=FLASH_WIDTH)
    canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

    canvas.front_img = PhotoImage(file="images/card_front.png")
    canvas.back_img = PhotoImage(file="images/card_back.png")
    
    canvas.card_bg_img = canvas.create_image(
        0.5*FLASH_WIDTH,
        0.5*FLASH_HEIGHT,
        image=canvas.front_img
    )

    canvas.grid(row=0, column=0, columnspan=2)

    canvas.label_text = canvas.create_text(LABEL_POS, text="English", font=FONT_LABEL)
    canvas.word_text = canvas.create_text(WORD_POS, text="Word", font=FONT_WORD)

    canvas.actual_word = next_card(words, canvas, window)

    img_wrong = PhotoImage(file="images/wrong.png")
    wrong_button = Button(image=img_wrong, highlightthickness=0,command=lambda: next_card(words, canvas, window))
    wrong_button.image = img_wrong

    wrong_button.grid(row=1, column=0)

    img_right = PhotoImage(file="images/right.png")
    right_button = Button(image=img_right, highlightthickness=0, command=lambda: right_action(words, canvas, window))
    right_button.image = img_right

    right_button.grid(row=1, column=1)

    return canvas

def read_words_from_csv():
    file = Path(WORDS_TO_LEARN_CSV)

    if file.exists():
        words_df = pandas.read_csv(WORDS_TO_LEARN_CSV)
    else:
        words_df = pandas.read_csv(MAIN_CSV)
        
    words_list = words_df.to_dict(orient="records")
    
    return words_list
    
def main():
    window = Tk()
    window.title("Flashy")
    window.config(padx=WINDOW_PADDING, pady=WINDOW_PADDING, bg=BACKGROUND_COLOR)
    
    words_pl_en = read_words_from_csv()
    init_UI(words_pl_en, window)
    
    window.mainloop()
    
main()

