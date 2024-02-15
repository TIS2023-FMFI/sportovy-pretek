import sys
from dataclasses import dataclass, asdict, field, fields

import tomli

import tomli_w

from .constants import CONFIG_FILE_PATH


@dataclass
class Config:
    API_KEY: str = field(init=False, repr=False, default="")
    API_ENDPOINT: str = field(init=False, default="https://is.orienteering.sk/api")
    API_CLUB_ID: int = field(init=False, default=46)
    WEB_APP_URL: str = field(init=False, default="http://localhost:8080/pehapezor.php")

    def __post_init__(self):
        self._load_config()

    def _create_example_config(self):
        if not CONFIG_FILE_PATH.is_file():
            CONFIG_FILE_PATH.touch(mode=0o640, exist_ok=True)
        self._save_config()
        exit_msg = (f"Konfigurácia sa nenašla. Prázdna konfigurácia bola vytvorená v {CONFIG_FILE_PATH}. "
                    "Nakonfigurujte si aplikáciu príkazom:"
                    "python -m orienter configure")
        sys.exit(exit_msg)

    def _load_config(self):
        if not CONFIG_FILE_PATH.is_file():
            self._create_example_config()
        with open(CONFIG_FILE_PATH, 'rb') as f:
            config_dict = tomli.load(f)
            for fld in fields(self):
                try:
                    setattr(self, fld.name, config_dict[fld.name])
                    if not config_dict[fld.name]:
                        print(f"POZOR: hodnota pre kľúč {fld.name} v konfigurácii je zrejme nevyplnená!")
                except KeyError:
                    sys.exit(f"Nepodarilo sa prečítať konfiguráciu, požadovaný kľúč sa nenašiel: {fld.name}")

    def _save_config(self):
        with open(CONFIG_FILE_PATH, 'wb') as f:
            tomli_w.dump(asdict(self), f)


configuration = Config()
