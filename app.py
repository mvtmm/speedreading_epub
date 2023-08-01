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
        self.base_font_size = 48
        self.word_label = tk.Label(self, font=("Helvetica", self.base_font_size))
        self.word_label.grid(row=0, column=0, sticky='ew') 
        self.words_per_minute = 300
        self.words_at_a_time = 1
        self.pause_reading = False
        self.stop_reading = Event()
        self.chapter_dropdown = None


        self.bind("<space>", self.toggle_pause)  # Bind space key to toggle_pause
        self.bind("<Up>", self.increase_speed)  # Bind up arrow key to increase_speed
        self.bind("<Down>", self.decrease_speed) # Bind down arrow key to decrease speed

        self.start_button = tk.Button(self, text="Start", command=self.start_reading)
        self.start_button.grid(row=1, column=0, pady=10)

        self.pause_button = tk.Button(self, text="Pause", command=self.toggle_pause)
        self.pause_button.grid(row=2, column=0, pady=10)

        self.settings_button = tk.Button(self, text="Settings", command=self.open_settings)
        self.settings_button.grid(row=3, column=0, pady=10)

        self.wpm_label = tk.Label(self, text=f"WPM: {self.words_per_minute}")
        self.wpm_label.grid(row=4, column=0, pady=10)

        self.reset_button = tk.Button(self, text="Reset", command=self.reset)
        self.reset_button.grid(row=6, column=0, pady=10)
        self.grid_columnconfigure(0, weight=1) 

    def increase_speed(self, event):
        self.words_per_minute += 20
        self.wpm_label.config(text=f"WPM: {self.words_per_minute}")

    def decrease_speed(self, event):
        self.words_per_minute -= 20
        if self.words_per_minute < 20:  # Prevent speed from going below 20
            self.words_per_minute = 20
        self.wpm_label.config(text=f"WPM: {self.words_per_minute}")

    def start_reading(self):
        epub_file = filedialog.askopenfilename(filetypes=[("EPUB files", "*.epub")])
        book = epub.read_epub(epub_file)
        chapters = [item for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT)]
        chapter_names = [item.get_name() for item in chapters]
        
        def select_chapter(*args):
            chapter_name = chapter_var.get()
            if chapter_name == "Choose Chapter":
                return
            index = chapter_names.index(chapter_name)
            text = chapters[index].get_content().decode('utf-8')
            soup = BeautifulSoup(text, 'html.parser')
            text = ''.join(ch for ch in soup.get_text() if ch.isprintable() or ch.isspace())
            self.stop_reading.set()  # Stop any ongoing speed reading
            self.stop_reading.clear()  # Reset the stop flag
            Thread(target=self.speed_read, args=(text,)).start()

        chapter_var = tk.StringVar(self)
        chapter_var.set("Choose Chapter")  # Set the initial value
        chapter_var.trace('w', select_chapter)
        self.chapter_dropdown = tk.OptionMenu(self, chapter_var, *chapter_names)
        if self.chapter_dropdown is not None:
            self.chapter_dropdown.grid_forget()  
            self.chapter_dropdown = tk.OptionMenu(self, chapter_var, *chapter_names)
            self.chapter_dropdown.grid(row=5, column=0, pady=10) 

    def reset(self):
        self.stop_reading.set()  # Stop any ongoing speed reading
        self.stop_reading.clear()  # Reset the stop flag
        if self.chapter_dropdown is not None:
            self.chapter_dropdown.grid_forget()  # Remove the dropdown menu
            self.chapter_dropdown = None

            
    def speed_read(self, text):
        for i in range(3, 0, -1):  # Countdown from 3 to 1
            self.word_label.config(text=str(i))
            time.sleep(1)
        self.word_label.config(text="Go!")
        time.sleep(1)
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


    def toggle_pause(self, event=None):
        self.pause_reading = not self.pause_reading

    def open_settings(self):
        self.words_per_minute = simpledialog.askinteger("Settings", "Words per minute:", initialvalue=self.words_per_minute)
        self.words_at_a_time = simpledialog.askinteger("Settings", "Words at a time:", initialvalue=self.words_at_a_time)
        self.wpm_label.config(text=f"WPM: {self.words_per_minute}")  # Update the label after changing the settings

# Example usage:
app = SpeedReader()
app.mainloop()
