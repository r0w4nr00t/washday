import os

from .misc import yaml_coarce


def get_settings_from_environment(prefix):
    prefix_len = len(prefix)
    return {key[prefix_len]: yaml_coarce(value) for key, value in os.environ.items() if key.startswith(prefix)}
