from pathlib import Path

import toml
from dataclasses import dataclass, asdict, field, fields
from .constants import CONFIG_FILE_PATH


@dataclass
class Config:
    API_KEY: str = field(init=False, repr=False, default="")
    API_ENDPOINT: str = field(init=False, default="https://is.orienteering.sk/api")
    API_CLUB_ID: int = field(init=False, default=46)
    DATABASE_PATH: str = field(init=False, default="")
    WEB_APP_URL: str = field(init=False, default="http://localhost:8080/pehapezor.php")

    def __post_init__(self):
        self._load_config()

    def _create_example_config(self):
        if not CONFIG_FILE_PATH.is_file():
            CONFIG_FILE_PATH.touch(mode=0o640, exist_ok=True)
        self._save_config()
        raise FileNotFoundError(f"No config file found. An empty one has been created at {CONFIG_FILE_PATH}.")

    def _load_config(self):
        if not CONFIG_FILE_PATH.is_file():
            self._create_example_config()
        with open(CONFIG_FILE_PATH, 'r') as f:
            config_dict = toml.load(f)
            for fld in fields(self):
                try:
                    setattr(self, fld.name, config_dict[fld.name])
                except KeyError:
                    raise SyntaxError(f"Failed to parse config file. Required entry {fld.name} not found.")

    def _save_config(self):
        with open(CONFIG_FILE_PATH, 'w') as f:
            toml.dump(asdict(self), f)


configuration = Config()
