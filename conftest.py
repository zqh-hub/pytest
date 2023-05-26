import pytest
from common.yaml_utils import YamlUtil


@pytest.fixture(scope="session", autouse=True)
def clear_extract():
    # 请求前清空
    YamlUtil.clear_extract_yaml()
