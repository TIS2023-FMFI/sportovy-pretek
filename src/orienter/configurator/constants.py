from pathlib import Path

from xdg_base_dirs import xdg_config_home

CONFIG_FILE_PATH: Path = xdg_config_home() / "orienter.toml"
