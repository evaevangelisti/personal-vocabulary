import requests
from bs4 import BeautifulSoup

def get_meanings(word):
    """
    Get meanings of a word from the wwww.dizionario-italiano.it

    Args:
    word (str): word to get meanings of

    Returns:
    (list): meanings of the word
    """
    
    url = f"https://www.dizionario-italiano.it/dizionario-italiano.php?lemma={word}100" # Considerare il caso in cui non è 100

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    return ["".join(element.text for element in meaning.children if isinstance(element, str) or element.name in ["a", "b", "i"]).strip() for meaning in soup.find_all("span", class_="italiano")]
