import yaml


def yaml_coarce(value):
    # convert value to proper python
    if isinstance(value, str):
        return yaml.load(f'dummy: {value}', loader=yaml.SafeLoader)['dummy']
    return value
