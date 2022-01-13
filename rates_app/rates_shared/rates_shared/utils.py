from typing import Any
import pathlib
import yaml


def read_config() -> Any:
    """ read config """

    with open(pathlib.Path(
            "config", "rates_config.yaml")) as yaml_file:

        return yaml.load(yaml_file, Loader=yaml.SafeLoader)
