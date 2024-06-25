import os
import json

def read_data(path: str) -> dict[str, list[str]]:
    """
    Read data from JSON file

    Args:
    path (str): path of the JSON file

    Returns:
    data (dict): data from JSON file
    """

    if not os.path.exists(path):
        return {}
    
    with open(path, "r") as file:
        try:
            data = json.load(file)

            if not isinstance(data, dict):
                print("Error: Failed to parse JSON file.")
                exit()
            
            for word, meanings in data.items():   
                if not isinstance(word, str) and not isinstance(meanings, list):
                    print("Error: Failed to parse JSON file.")
                    exit()
                
                for meaning in meanings:
                    if not isinstance(meaning, str):
                        print("Error: Failed to parse JSON file.")
                        exit()
        except json.JSONDecodeError:
            return {}
                       
        return data

def write_data(path: str, data: dict[str, list[str]]):
    """
    Write data to JSON file

    Args:
    path (str): path of the JSON file
    data (dict): data to write to JSON file
    """

    with open(path, "w") as file:
        json.dump(data, file, indent=4)