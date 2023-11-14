import tomllib
from dataclasses import dataclass, asdict, field, fields
from .constants import CONFIG_FILE_PATH

import tomli_w


@dataclass(kw_only=True)
class Config:
    API_KEY: str = field(init=False, repr=False, default="")
    API_ENDPOINT: str = field(init=False, default="https://is.orienteering.sk/api")
    DATABASE_PATH: str = field(init=False, default="")

    def __post_init__(self):
        self._load_config()
        if not CONFIG_FILE_PATH.is_file():
            raise FileNotFoundError(f"Database file not found at {self.DATABASE_PATH}.")

    def _create_example_config(self):
        if not CONFIG_FILE_PATH.is_file():
            CONFIG_FILE_PATH.touch(mode=0o660, exist_ok=True)
        self._save_config()
        raise FileNotFoundError(f"No config file found. An empty one has been created at {CONFIG_FILE_PATH}.")

    def _load_config(self):
        if not CONFIG_FILE_PATH.is_file():
            self._create_example_config()
        with open(CONFIG_FILE_PATH, 'rb') as f:
            config_dict = tomllib.load(f)
            for fld in fields(self):
                try:
                    setattr(self, fld.name, config_dict[fld.name])
                except KeyError:
                    raise SyntaxError(f"Failed to parse config file. Required entry {fld.name} not found.")

    def _save_config(self):
        with open(CONFIG_FILE_PATH, 'wb') as f:
            tomli_w.dump(asdict(self), f)


configuration = Config()
