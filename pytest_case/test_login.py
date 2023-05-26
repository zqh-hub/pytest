import pytest
from common.yaml_utils import YamlUtil
from common.request_util import RequestUtil


class TestLogin:
    @pytest.mark.parametrize('args_sms', YamlUtil.read_cases("sms.yaml"))
    def test_sms_token(self, args_sms):
        response = RequestUtil.send_request(method=args_sms["request"]["method"], url=args_sms["request"]["url"],
                                            headers=args_sms["request"]["headers"], json=args_sms["request"]["data"])
        sms_token = response.json().get("data", None)
        print(sms_token)
        if sms_token is not None:
            YamlUtil.write_extract_yaml({"sms_token": sms_token})

    @pytest.mark.parametrize("args_login", YamlUtil.read_cases("login.yaml"))
    def test_login(self, args_login):
        sms_token = YamlUtil.read_extract_yaml("sms_token")
        args_login["request"]["data"]["sms_token"] = sms_token
        response = RequestUtil.send_request(method=args_login["request"]["method"], url=args_login["request"]["url"],
                                            headers=args_login["request"]["headers"],
                                            json=args_login["request"]["data"])
        print(response.json())
