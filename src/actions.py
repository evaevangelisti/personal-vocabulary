import curses

def add_term(stdscr, vocabulary):
    stdscr.erase()

    stdscr.addstr(0, 0, "Add term", curses.A_BOLD)
    stdscr.addstr(2, 0, "Enter the new word:")
    stdscr.addstr(3, 0, "")

    curses.curs_set(1)

    word = ""
    x = 0

    while True:
        key = stdscr.getch()

        match key:
            case key if 65 <= key <= 90 or 97 <= key <= 122:
                character = chr(key)

                stdscr.addstr(3, x, character)

                word += character.lower()
                x += 1

            case 27: 
                curses.curs_set(0)
                return 
            
            case 10 | 13 | curses.KEY_ENTER:
                curses.curs_set(0)
                break

            case _:
                pass

    if vocabulary.search_term(word) != -1:
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(5, 0, f"Word '{word}' already exists")
        stdscr.attroff(curses.color_pair(3))

    term = vocabulary.add_term(word)

    if term:
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(5, 0, f"Word '{word}' added successfully")
        stdscr.attroff(curses.color_pair(2))
    else:
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(5, 0, f"Word '{word}' does not exist")
        stdscr.attroff(curses.color_pair(3))

    stdscr.getch()

def edit_meanings(stdscr, vocabulary):
    pass

def remove_term(stdscr, vocabulary):
    pass

def search_term(stdscr, vocabulary):
    pass

def display_vocabulary(stdscr, vocabulary):
    pass

def train(stdscr, vocabulary):
    pass

def retrieve_actions(stdscr, vocabulary):
    return {
        "Add term": lambda: add_term(stdscr, vocabulary),
        "Edit meanings": lambda: edit_meanings(stdscr, vocabulary),
        "Remove term": lambda: remove_term(stdscr, vocabulary),
        "Search term": lambda: search_term(stdscr, vocabulary),
        "Display your own vocabulary": lambda: display_vocabulary(stdscr, vocabulary),
        "Train": lambda: train(stdscr, vocabulary),
    }