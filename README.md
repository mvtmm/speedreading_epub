# SpeedReader

SpeedReader is a Python application that helps you improve your reading speed by displaying a book's content at a configurable speed. You can control the number of words displayed at a time, the speed at which they are displayed, and the ability to pause and resume reading. The application uses a graphical user interface provided by the Tkinter library.

![Screenshot of the application](screenshot.png)

## Installation

Before running the program, you need to install a few dependencies. You can do this by running the following command in your terminal:

```bash
pip install ebooklib beautifulsoup4
```

## Usage

To use the application, simply run the Python script:

```bash
python speedreader.py
```

This will open a GUI window with several options:

- "Start": Click this button to select an EPUB file. Once the file is selected, a dropdown menu will appear, allowing you to select a chapter.
- "Pause": Click this button to pause and resume the reading.
- "Settings": Click this button to open a dialog where you can set the number of words displayed at a time and the speed at which they are displayed (in words per minute).
- "Reset": Click this button to stop the reading and remove the chapter selection dropdown.

You can also use the following keyboard shortcuts:

- Space: Pause/resume the reading.
- Up arrow: Increase the reading speed by 20 words per minute.
- Down arrow: Decrease the reading speed by 20 words per minute.

The current reading speed (in words per minute) is displayed below the "Settings" button.

## Dependencies

- Python 3
- Tkinter
- ebooklib
- BeautifulSoup4

## Author

Marvin Timm

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details
