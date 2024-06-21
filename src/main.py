import curses

from menu import Menu
from actions import retrieve_actions
from vocabulary import Vocabulary

def main(stdscr):
    vocabulary = Vocabulary()
    actions = retrieve_actions(stdscr, vocabulary)

    menu = Menu(stdscr, actions)
    menu.run()

if __name__ == "__main__":
    curses.wrapper(main)