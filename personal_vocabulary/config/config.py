import os
import json
from appdirs import user_config_dir, user_data_dir

APP_NAME = "PersonalVocabulary"
APP_AUTHOR = "Eva"

class Config:
    def __init__(self):
        """
        Initialize the configuration
        """

        self._config_path = user_config_dir(APP_NAME, APP_AUTHOR)
        self._config_file = "config.json"

        self._data_path = user_data_dir(APP_NAME, APP_AUTHOR)
        self._data_file = "vocabulary.json"

        self._config = self._load()

    def _write(self, config: dict[str, str]) -> None:
        """
        Write the configuration to a JSON file

        Args:
        config (dict): configuration to write
        """

        with open(os.path.join(self._config_path, self._config_file), "w") as file:
            json.dump(config, file, indent=4)

    def _load(self) -> dict[str, str]:
        """
        Load the configuration from a JSON file
        
        Returns:
        (dict): configuration
        """
        
        os.makedirs(self._config_path, exist_ok=True)

        config = {
            "path": os.path.join(self._data_path, self._data_file)
        }

        if not os.path.exists(os.path.join(self._config_path, self._config_file)):
            os.makedirs(self._data_path, exist_ok=True)
            self._write(config)
        else:
            with open(os.path.join(self._config_path, self._config_file), "r") as file:
                try:
                    config = json.load(file)
                except json.JSONDecodeError:
                    os.makedirs(self._data_path, exist_ok=True)
                    self._write(config)
        print(f"config: {config}")
        return config

    def get_path(self) -> str:
        """
        Get the path of the vocabulary data
        
        Returns:
        (str): path of the vocabulary data
        """

        return self._config.get("path")