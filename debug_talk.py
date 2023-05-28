import random
from common.yaml_utils import YamlUtil


class DebugTalk:
    @staticmethod
    def get_extract(extract_name):
        return YamlUtil.read_extract_yaml(extract_name)

    @staticmethod
    def random_num(num_min, num_max):
        return random.randint(int(num_min), int(num_max))
