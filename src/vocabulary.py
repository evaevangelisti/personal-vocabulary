import bisect

from storage import read_data, write_data
from scraper import get_meanings

class Vocabulary:
    def __init__(self):
        """
        Initialize the vocabulary and sort it

        Returns:
        (Vocabulary): vocabulary initialized and sorted
        """
        
        self._data = read_data()
        self._data.sort(key=lambda term: term["word"])

    def add_term(self, word):
        """
        Add a term to the vocabulary

        Args:
        word (str): word to add to the vocabulary
        """

        meanings = get_meanings(word)

        if not meanings:
            return
        
        bisect.insort(self._data, {"word": word, "meanings": meanings})

        write_data(self._data)
    
    def edit_meanings(self, index, meanings):
        """
        Edit meanings of a term in the vocabulary

        Args:
        index (int): index of the term to edit
        meanings (list): meanings to set to the term
        """

        self._data[index]["meanings"] = meanings

        write_data(self._data)
    
    def delete_term(self, index):
        """
        Delete a term from the vocabulary

        Args:
        index (int): index of the term to delete
        """

        del self._data[index]

        write_data(self._data)

    def search_term(self, word):
        """
        Find a term in the vocabulary by its word

        Args:
        word (str): word of the term to find

        Returns:
        (int): index of the term in the vocabulary
        """

        words = [term["word"] for term in self._data]

        index = bisect.bisect_left(words, word)

        return index if index < len(words) and words[index] == word else -1
    
    def get_terms(self):
        """
        Get all the terms in the vocabulary

        Returns:
        (list): all terms in the vocabulary
        """

        return self._data

    def train(self):
        pass