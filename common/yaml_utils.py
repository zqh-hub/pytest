import os
import yaml


class YamlUtil:
    base_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]

    @staticmethod
    def read_extract_yaml(key):
        path = os.path.join(YamlUtil.base_path, "extract.yaml")
        with open(path, 'r', encoding="utf-8") as f:
            data = yaml.load(f, yaml.FullLoader)
            return data[key]

    @staticmethod
    def write_extract_yaml(data):
        path = os.path.join(YamlUtil.base_path, "extract.yaml")
        with open(path, 'w', encoding="utf-8") as f:
            yaml.dump(data, stream=f, allow_unicode=True)

    @staticmethod
    def clear_extract_yaml():
        path = os.path.join(YamlUtil.base_path, "extract.yaml")
        with open(path, 'w', encoding="utf-8") as f:
            yaml.dump("", stream=f, allow_unicode=True)

    @staticmethod
    def read_config_yaml(one_node, two_node):
        path = os.path.join(YamlUtil.base_path, "config.yaml")
        with open(path, 'r', encoding="utf-8") as f:
            data = yaml.load(f, yaml.FullLoader)
            return data[one_node][two_node]

    @staticmethod
    def read_cases(yaml_name):
        case_path = os.path.join(YamlUtil.base_path, os.path.join("cases", yaml_name))
        with open(case_path, 'r', encoding="utf-8") as f:
            data = yaml.load(f, yaml.FullLoader)
            return data
