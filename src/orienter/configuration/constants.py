from pathlib import Path

from xdg import xdg_config_home, xdg_data_home

CONFIG_FILE_PATH: Path = xdg_config_home() / "orienter.toml"
XDG_DATA_HOME: Path = xdg_data_home()
