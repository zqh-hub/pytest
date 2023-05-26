import pytest
import requests
from common.yaml_utils import read_yaml


@pytest.mark.parametrize('data', read_yaml("../data/user.yaml"))
def test_01(data):
    url = "http://wallet-dashboard.pinpula.com/pingpp/users/login"
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.request("post", url=url, headers=headers, json=data["user"])
    assert response.json().get("message") == data["msg"]
    print(response.text)


if __name__ == '__main__':
    pytest.main(["-vs"])
