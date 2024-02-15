from pathlib import Path

from xdg import xdg_config_home

CONFIG_FILE_PATH: Path = xdg_config_home() / "orienter.toml"
