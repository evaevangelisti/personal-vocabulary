import sys
import os
import curses

from src.menu import Menu
from src.vocabulary import Vocabulary
from src.storage import read_data

from config.config import Config

def main(stdscr: curses.window) -> None:
    config = Config()    
    path = config.get_path()

    vocabulary = Vocabulary(path)

    menu = Menu(stdscr, vocabulary, 5)
    menu.run()

if __name__ == "__main__":
    try:
        os.environ.setdefault("ESCDELAY", "25")
        curses.wrapper(main)
    except KeyboardInterrupt:
        curses.echo()
        curses.cbreak()
        curses.endwin()

        sys.exit()