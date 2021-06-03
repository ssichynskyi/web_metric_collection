# -*- coding: utf-8 -*-
import os
from pathlib import Path

import yaml

from utils.dict_merger import merge_dicts


class ConfigParser:
    """Extracts the data from the configuration file given."""
    def __new__(cls, path):
        with open(path, 'r') as f:
            contents = f.read()
            return yaml.safe_load(contents)


_path_to_config = Path(os.environ['COLLECTION_CONFIG'])
_path_to_local_config = Path(os.environ['COLLECTION_CONFIG_LOCAL'])
config = ConfigParser(_path_to_config)
_config_local = ConfigParser(_path_to_local_config)
config = merge_dicts(config, _config_local)
