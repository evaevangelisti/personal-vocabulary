import os
import json

from config import path

# Modificare l'error handling
def read_data():
    """
    Read data from JSON file

    Returns:
    data (dict): data from JSON file
    """

    if not os.path.exists(path):
        return []
    
    with open(path, 'r') as file:
        data = json.load(file)

        if not isinstance(data, list):
            return []
        
        for term in data:
            if not isinstance(term, dict):
                return []
            
            if "word" not in term and "meanings" not in term:
                return []
            
            if not isinstance(term["word"], str) and not isinstance(term["meanings"], list):
                return []
            
            for meaning in term["meanings"]:
                if not isinstance(meaning, str):
                    return []
                       
        return data

def write_data(data):
    """
    Write data to JSON file

    Args:
    data (dict): data to write to JSON file
    """

    with open(path, 'w') as file:
        json.dump(data, file, indent=4)