import time
import tkinter as tk
from tkinter import filedialog
from threading import Thread

class SpeedReader(tk.Tk):
    def __init__(self, words_per_minute=200):
        super().__init__()
        self.words_per_minute = words_per_minute
        self.word_label = tk.Label(self, font=("Helvetica", 48))
        self.word_label.pack(pady=20)

        self.start_button = tk.Button(self, text="Start", command=self.start_reading)
        self.start_button.pack(pady=20)

    def start_reading(self):
        text_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        with open(text_file, 'r') as f:
            text = f.read()
        Thread(target=self.speed_read, args=(text,)).start()

    def speed_read(self, text):
        words = text.split() # Split the text into words
        words_per_second = self.words_per_minute / 60 # Calculate the words per second
        for word in words:
            self.word_label.config(text=word)
            time.sleep(1/words_per_second) # Pause for the appropriate time

# Example usage:
app = SpeedReader(words_per_minute=200)
app.mainloop()
