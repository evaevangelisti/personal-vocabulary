from sortedcontainers import SortedDict

from src.storage import read_data, write_data
from src.scraper import get_meanings

class Vocabulary:
    def __init__(self, path: str) -> None:
        """
        Initialize the vocabulary and sort it

        Args:
        data (dict): data of the vocabulary
        """
        
        self._path = path
        self._data = SortedDict(read_data(path))

        write_data(self._path, self._data)

    def get_terms(self, prefix: str = "") -> dict[str, list[str]]:
        """
        Get all the terms in the vocabulary

        Args:
        prefix (str): prefix to filter the terms

        Returns:
        (dict): all terms in the vocabulary
        """

        return SortedDict({word: meanings for word, meanings in self._data.items() if word.startswith(prefix)})

    def get_meanings(self, word: str) -> list[str]:
        """
        Get meanings of a term in the vocabulary

        Args:
        word (str): word of the term to get meanings

        Returns:
        (list): meanings of the term
        """

        if word not in self._data:
            return []

        return self._data[word].copy()

    def add_term(self, word: str) -> bool:
        """
        Add a term to the vocabulary

        Args:
        word (str): word to add to the vocabulary

        Returns:
        (bool): whether the term is added successfully
        """

        meanings = get_meanings(word)

        if not meanings:
            return False
        
        self._data[word] = meanings
        write_data(self._path, self._data)

        return True
    
    def set_meanings(self, word: str, meanings: list[str]) -> None:
        """
        Set meanings of a term in the vocabulary

        Args:
        word (str): word of the term to set
        meanings (list): meanings to set to the term
        """

        if word in self._data:
            self._data[word] = meanings
            write_data(self._path, self._data)
    
    def remove_term(self, word: str) -> None:
        """
        Remove a term from the vocabulary

        Args:
        word (str): word of the term to remove
        """

        if word in self._data:
            del self._data[word]
            write_data(self._path, self._data)