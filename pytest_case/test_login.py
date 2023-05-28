import pytest
from common.yaml_utils import YamlUtil
from common.request_util import RequestUtil


class TestLogin:
    @pytest.mark.parametrize('args_sms', YamlUtil.read_cases("sms.yaml"))
    def test_sms_token(self, args_sms):
        response = RequestUtil().check_yaml(args_sms)
        print(response.json())

    @pytest.mark.parametrize("args_login", YamlUtil.read_cases("login.yaml"))
    def test_login(self, args_login):
        response = RequestUtil().check_yaml(args_login)
        print(response.json())
