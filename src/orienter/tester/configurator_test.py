import os
import unittest
from dataclasses import fields

import tomli

from ..configurator.config import Config
from ..configurator.constants import *


class ConfigTestCase(unittest.TestCase):
    def test_config_file_path_permissions(self):
        self.assertTrue(
            os.access(CONFIG_FILE_PATH, os.R_OK | os.W_OK, effective_ids=True),
            "missing read or write permission for config file",
        )

    def test_config_file(self):
        original_config_file_path = CONFIG_FILE_PATH.parent / "orienter.toml.bak"
        if CONFIG_FILE_PATH.is_file():
            os.rename(CONFIG_FILE_PATH, original_config_file_path)
        try:
            _ = Config(output=False)
        except SystemExit:
            config = Config(output=False)
            with open(CONFIG_FILE_PATH, "rb") as f:
                config_dict = tomli.load(f)
                for fld in fields(Config):
                    self.assertEqual(
                        getattr(config, fld.name), config_dict[fld.name], "unexpected value of config file item"
                    )
        finally:
            os.remove(CONFIG_FILE_PATH)
            os.rename(original_config_file_path, CONFIG_FILE_PATH)
