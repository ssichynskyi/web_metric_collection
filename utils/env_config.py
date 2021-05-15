# -*- coding: utf-8 -*-

import yaml

from pathlib import Path

CONFIG_PATH = 'config'
"""path to config files folder from project root"""


class ConfigParser:
    """Extracts the data from the configuration file given"""
    def __new__(cls, path):
        with open(path, 'r') as f:
            contents = f.read()
            return yaml.safe_load(contents)


_path_to_config = Path(__file__).parent.parent.joinpath(CONFIG_PATH, 'hosts.yaml')
config = ConfigParser(_path_to_config)
