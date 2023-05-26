import json
import requests
from common.yaml_utils import YamlUtil


class RequestUtil:
    sess = requests.session()
    base_url = YamlUtil.read_config_yaml("base", "base_url")

    @staticmethod
    def send_request(method, url, data=None, **kwargs):
        method = str(method).lower()
        full_url = RequestUtil.base_url + url
        res = None
        if method == "get":
            res = RequestUtil.sess.request(method=method, url=full_url, params=data, **kwargs)
        elif method == "post":
            if data and isinstance(data, dict):
                data = json.dumps(data)
            res = RequestUtil.sess.request(method=method, url=full_url, data=data, **kwargs)
        else:
            pass
        return res
