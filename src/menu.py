import curses

class Menu:
    def __init__(self, stdscr, actions):
        """
        Initialize the menu

        Args:
        stdscr (curses.window): standard screen
        actions (dict): actions of the menu
        """

        self._stdscr = stdscr
        self._actions = actions
        self._selected = 0
        
    def _display(self):
        """
        Display the menu
        """

        self._stdscr.erase()

        self._stdscr.addstr(0, 0, "Personal Vocabulary", curses.A_BOLD)
        self._stdscr.addstr(2, 0, "Select an action:")

        for index, action in enumerate(self._actions):
            if index == self._selected:
                self._stdscr.attron(curses.color_pair(1))
                self._stdscr.addstr(index + 3, 0, f"> {action}")
                self._stdscr.attroff(curses.color_pair(1))
            else:
                self._stdscr.addstr(index + 3, 0, f"  {action}")

        self._stdscr.refresh()

    def _navigate(self, key):
        """
        Navigate the menu

        Args:
        key (int): key pressed
        """

        match key:
            case curses.KEY_UP:
                if self._selected > 0:
                    self._selected -= 1

            case curses.KEY_DOWN:
                if self._selected < len(self._actions) - 1:
                    self._selected += 1

            case 10 | 13 | curses.KEY_ENTER:
                self._actions[list(self._actions)[self._selected]]()

            case curses.KEY_RESIZE:
                curses.resize_term(0, 0)
                
            case 27:
                exit()

            case _:
                return

        self._display()

    def run(self):
        """
        Run the menu
        """

        curses.curs_set(0)

        curses.start_color()

        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        self._display()

        while True:
            key = self._stdscr.getch()
            self._navigate(key)