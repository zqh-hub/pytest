import yaml


def read_yaml(path):
    with open(path, 'r', encoding="utf-8") as f:
        data = yaml.load(f, yaml.FullLoader)
        return data
