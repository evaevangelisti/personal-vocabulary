from enum import Enum, auto
import curses
import random

class Mode(Enum):
    TERM = auto()
    ACTION = auto()

class Menu:
    def __init__(self, stdscr: curses.window, vocabulary: dict[str, list[str]], words_to_display: int) -> None:
        """
        Initialize the menu

        Args:
        stdscr (curses.window): standard screen
        actions (dict): actions of the menu
        """

        self._stdscr = stdscr
        self._vocabulary = vocabulary
        self._range = {"start": 0, "end": words_to_display}
        self._mode = Mode.TERM
        self._word_selected = vocabulary.get_terms().keys()[0] if vocabulary.get_terms() else ""
        self._word_filter = ""

    def _display_menu(self) -> None:
        """
        Display the menu
        """

        self._stdscr.erase()

        self._stdscr.addstr(0, 0, "Personal Vocabulary", curses.A_BOLD)

        words = self._vocabulary.get_terms(self._word_filter.lower()).keys()
        words_to_display = self._range["end"] - self._range["start"]

        action = "Search:" if words else "Add:"

        self._stdscr.addstr(1, 0, action)
        self._stdscr.addstr(1, len(action) + 1, self._word_filter)

        y_cursor, x_cursor = self._stdscr.getyx()

        if words:
            if self._word_selected not in words:
                self._word_selected = words[0]

            word_selected_index = words.index(self._word_selected)

            if word_selected_index < self._range["start"]:
                self._range["start"] = word_selected_index
                self._range["end"] = word_selected_index + words_to_display

            if word_selected_index >= self._range["end"]:
                self._range["start"] = word_selected_index - words_to_display + 1
                self._range["end"] = word_selected_index + 1

            for i, word in enumerate(words[self._range["start"]:min(self._range["end"], len(words))]):
                if word == self._word_selected:
                    if self._mode == Mode.TERM:
                        self._stdscr.addstr(i + 3, 0, f"> {word.capitalize()}", curses.color_pair(1))
                    else:
                        self._stdscr.addstr(i + 3, 0, f"> {word.capitalize()}")
                else:
                    self._stdscr.addstr(i + 3, 0, f"  {word.capitalize()}")

        self._stdscr.addstr(words_to_display + 4, 0, "Actions", curses.A_BOLD)
        
        if self._mode == Mode.ACTION:
            self._stdscr.addstr(words_to_display + 5, 0, "Train", curses.color_pair(1))
        else:
            self._stdscr.addstr(words_to_display + 5, 0, "Train")
        
        self._stdscr.move(y_cursor, x_cursor)

    def _display_term(self, word: str) -> None:
        """
        Display term

        Args:
        word (str): word to display
        """

        curses.curs_set(0)

        self._stdscr.erase()
        
        self._stdscr.addstr(0, 0, f"{word.capitalize()}", curses.A_BOLD)

        height, width = self._stdscr.getmaxyx()

        meanings = self._vocabulary.get_meanings(word)

        lines = []

        for meaning in meanings:
            line = ""

            for word in meaning.split():
                if len(line + word) >= width - 2:
                    lines.append(line.strip())
                    line = ""

                line += f"{word} "

            if line:
                lines.append(line.strip())

        start, end = 0, 10

        while True:
            for i, line in enumerate(lines[start:end]):
                self._stdscr.move(i + 2, 0)
                self._stdscr.clrtoeol()

                if any(meaning.startswith(line) for meaning in meanings):
                    self._stdscr.addstr(i + 2, 0, "-")

                self._stdscr.addstr(i + 2, 2, line)

            key = self._stdscr.getch()

            match key:
                case curses.KEY_UP:
                    if start > 0:
                        start -= 1
                        end -= 1

                case curses.KEY_DOWN:
                    if end < len(lines):
                        start += 1
                        end += 1

                case curses.KEY_RESIZE:
                    pass # Manage resize

                case 27:
                    break

                case _:
                    pass

    def _train(self) -> None:
        """
        
        """

        curses.curs_set(1)

        self._stdscr.erase()

        self._stdscr.addstr(3, 0, "Meanings", curses.A_BOLD)
        self._stdscr.addstr(10, 0, "Actions", curses.A_BOLD)

        height, width = self._stdscr.getmaxyx()

        while True:
            words = list(self._vocabulary.get_terms().keys())
            random.shuffle(words)

            for word in words:
                meanings = self._vocabulary.get_meanings(word)

                guess_mode = True
                incorrect = True

                lines = []
                start, end = 0, 5

                guess = ""

                while True:
                    if incorrect and meanings:
                        meaning = random.choice(meanings)
                        meanings.remove(meaning)

                        line = ""

                        for substring in meaning.split():
                            if len(line + substring) >= width - 2:
                                lines.append(line.strip())
                                line = ""

                            line += f"{substring} "

                        if line:
                            lines.append(line.strip())

                        incorrect = False

                    for i, line in enumerate(lines[start:end]):
                        self._stdscr.move(i + 4, 0)
                        self._stdscr.clrtoeol()

                        if any(meaning.startswith(line) for meaning in self._vocabulary.get_meanings(word)):
                            self._stdscr.addstr(i + 4, 0, "-")

                        self._stdscr.addstr(i + 4, 2, line)

                    if guess_mode:
                        self._stdscr.addstr(11, 0, "Solution")
                    else:
                        self._stdscr.addstr(11, 0, "Solution", curses.color_pair(1))

                    self._stdscr.move(1, 0)
                    self._stdscr.clrtoeol()

                    self._stdscr.addstr(1, 0, f"Guess:", curses.A_BOLD)
                    self._stdscr.addstr(1, len("Guess:") + 1, f"{guess}")

                    key = self._stdscr.getch()

                    match key:
                        case key if 65 <= key <= 90 or 97 <= key <= 122:
                            if guess_mode:
                                guess += chr(key)

                        case 8 | 127 | curses.KEY_BACKSPACE:
                            if len(guess) > 0 and guess_mode:
                                guess = guess[:-1]

                        case curses.KEY_UP:
                            if start > 0 and guess_mode:
                                start -= 1
                                end -= 1

                        case curses.KEY_DOWN:
                            if end < len(lines) and guess_mode:
                                start += 1
                                end += 1

                        case 10 | 13 | curses.KEY_ENTER:
                            if not guess_mode: 
                                self._stdscr.addstr(11, 0, "Solution")
                                guess = word

                            if guess:
                                curses.curs_set(0)

                                if guess.lower() == word:
                                    self._stdscr.addstr(1, len("Guess:") + 1, guess, curses.color_pair(2))

                                    self._stdscr.getch()

                                    for i in range(4, 9):
                                        self._stdscr.move(i, 0)
                                        self._stdscr.clrtoeol()

                                    curses.curs_set(1)

                                    break
                                else:
                                    self._stdscr.addstr(1, len("Guess:") + 1, guess, curses.color_pair(3))

                                    self._stdscr.getch()

                                    guess = ""
                                    incorrect = True

                                    curses.curs_set(1)

                        case 9:
                            if guess_mode:
                                guess_mode = False
                                curses.curs_set(0)
                            else:
                                guess_mode = True
                                curses.curs_set(1)

                        case curses.KEY_RESIZE:
                            pass

                        case 27:
                            return
                        
                        case _:
                            pass

    def _navigate(self, key: int) -> bool:
        """
        Navigate the menu

        Args:
        key (int): key pressed

        Returns:
        (bool): whether to display the menu
        """

        match key:
            case key if 65 <= key <= 90 or 97 <= key <= 122:
                if self._mode == Mode.TERM:
                    self._word_filter += chr(key)

                    return True

            case 8 | 127 | curses.KEY_BACKSPACE:
                if len(self._word_filter) > 0 and self._mode == Mode.TERM:
                    self._word_filter = self._word_filter[:-1]

                    return True

            case curses.KEY_UP:
                if self._mode == Mode.TERM:
                    words = self._vocabulary.get_terms(self._word_filter.lower()).keys()

                    if words:
                        word_selected_index = words.index(self._word_selected)

                        if word_selected_index > 0:
                            self._word_selected = words[word_selected_index - 1]

                            return True

            case curses.KEY_DOWN:
                if self._mode == Mode.TERM:
                    words = self._vocabulary.get_terms(self._word_filter.lower()).keys()

                    if words:
                        word_selected_index = words.index(self._word_selected)

                        if word_selected_index < len(words) - 1:
                            self._word_selected = words[word_selected_index + 1]

                            return True

            case 10 | 13 | curses.KEY_ENTER:
                if self._mode == Mode.TERM:
                    terms = self._vocabulary.get_terms(self._word_filter.lower())

                    if terms:
                        self._display_term(self._word_selected)
                        curses.curs_set(1)
                    else:
                        if not self._vocabulary.add_term(self._word_filter.lower()):
                            curses.curs_set(0)

                            self._stdscr.addstr(3, 0, f"Word '{self._word_filter}' doesn't exist", curses.color_pair(3))

                            self._stdscr.getch()

                            self._word_filter = ""
                            curses.curs_set(1)
                else:
                    self._train()
                    curses.curs_set(0)

                return True
            
            case 9:
                if self._mode == Mode.TERM:
                    self._mode = Mode.ACTION

                    curses.curs_set(0)
                else:   
                    self._mode = Mode.TERM

                    curses.curs_set(1)

                return True

            case curses.KEY_RESIZE:
                pass # Manage resize
                
            case 27:
                if self._mode == Mode.TERM and self._word_filter:
                    self._word_filter = ""

                    return True

            case _:
                pass

        return False
            
    def run(self) -> None:
        """
        Run the menu
        """

        curses.start_color()
        curses.use_default_colors()

        curses.init_pair(1, curses.COLOR_BLUE, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_RED, -1)

        self._display_menu()

        while True:
            key = self._stdscr.getch()
            display = self._navigate(key)

            if display:
                self._display_menu()  