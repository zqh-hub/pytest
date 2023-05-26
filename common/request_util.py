import json

import requests


class RequestUtil:
    sess = requests.session()

    @staticmethod
    def send_request(method, url, data=None, **kwargs):
        method = str(method).lower()
        res = None
        if method == "get":
            res = RequestUtil.sess.request(method=method, url=url, params=data, **kwargs)
        elif method == "post":
            if data and isinstance(data, dict):
                data = json.dumps(data)
            res = RequestUtil.sess.request(method=method, url=url, data=data, **kwargs)
        else:
            pass
        return res
