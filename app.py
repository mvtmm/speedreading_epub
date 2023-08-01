import time
import tkinter as tk
from tkinter import filedialog, simpledialog
from threading import Thread, Event
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

class SpeedReader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")  # Set initial window size
        self.words_per_minute = 400
        self.words_at_a_time = 1
        self.pause_reading = False
        self.stop_reading = Event()
        self.word_label = tk.Label(self, font=("Helvetica", 48), width=10)
        self.word_label.pack(pady=20)

        self.start_button = tk.Button(self, text="Start", command=self.start_reading)
        self.start_button.pack(pady=20)

        self.pause_button = tk.Button(self, text="Pause", command=self.toggle_pause)
        self.pause_button.pack(pady=20)

        self.settings_button = tk.Button(self, text="Settings", command=self.open_settings)
        self.settings_button.pack(pady=20)

    def start_reading(self):
        epub_file = filedialog.askopenfilename(filetypes=[("EPUB files", "*.epub")])
        book = epub.read_epub(epub_file)
        chapters = [item for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT)]
        chapter_names = [item.get_name() for item in chapters]
        
        def select_chapter(*args):
            chapter_name = chapter_var.get()
            index = chapter_names.index(chapter_name)
            text = chapters[index].get_content().decode('utf-8')
            soup = BeautifulSoup(text, 'html.parser')
            text = ''.join(ch for ch in soup.get_text() if ch.isprintable() or ch.isspace())
            self.stop_reading.set()  # Stop any ongoing speed reading
            self.stop_reading.clear()  # Reset the stop flag
            Thread(target=self.speed_read, args=(text,)).start()

        chapter_var = tk.StringVar(self)
        chapter_var.trace('w', select_chapter)
        chapter_dropdown = tk.OptionMenu(self, chapter_var, *chapter_names)
        chapter_dropdown.pack()



    def speed_read(self, text):
        words = text.split() # Split the text into words
        for i in range(0, len(words), self.words_at_a_time):
            if self.stop_reading.is_set():
                break
            if self.pause_reading:
                while self.pause_reading:
                    time.sleep(0.1)
            word = " ".join(words[i:i+self.words_at_a_time])
            self.word_label.config(text=word)
            words_per_second = self.words_per_minute / 60 # Move this line here
            time.sleep(1/words_per_second) # Pause for the appropriate time


    def toggle_pause(self):
        self.pause_reading = not self.pause_reading

    def open_settings(self):
        self.words_per_minute = simpledialog.askinteger("Settings", "Words per minute:", initialvalue=self.words_per_minute)
        self.words_at_a_time = simpledialog.askinteger("Settings", "Words at a time:", initialvalue=self.words_at_a_time)

# Example usage:
app = SpeedReader()
app.mainloop()
