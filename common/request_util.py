import json
import re

import requests
import jsonpath
from common.yaml_utils import YamlUtil
from debug_talk import DebugTalk


class RequestUtil:
    sess = requests.session()
    base_url = YamlUtil.read_config_yaml("base", "base_url")

    def check_yaml(self, yaml_info: dict):
        # 1、校验必填字段：name、request、validate
        if "name" in yaml_info and "request" in yaml_info and "validate" in yaml_info:
            # 2、request中必填字段：method、url
            request_info = yaml_info.get("request")
            if "method" in request_info and "url" in request_info:
                method = request_info.pop("method")
                url = request_info.pop("url")
                headers = request_info.pop("headers", None)
                # 针对文件上传，获取到路径后，读取文件
                files = request_info.pop("'files", None)
                if files:
                    for key, value in files.items():
                        files[key] = open(value, "rb", encoding="utf-8")
                # 3、发起请求
                response = self.send_request(method, url, headers=headers, files=files, **request_info)
                self.extract(yaml_info, response)
                return response
            else:
                raise Exception("request必填字段校验失败！！")
        else:
            raise Exception("yaml必填字段校验失败！！")

    @staticmethod
    def extract(yaml_info: dict, response):
        if "extract" in yaml_info:
            extract_info = yaml_info["extract"]
            for key, value in extract_info.items():
                # 判断是正则表达式，还是jsonpath
                flag = value[0]
                if flag == "r":
                    extract_value = re.search(eval(value), response.text)
                    if extract_value:
                        extract_value = extract_value.group()
                        extract_data = {key: extract_value}
                    else:
                        raise Exception("正则：{}未匹配到".format(value))
                elif flag == "$":
                    extract_value = jsonpath.jsonpath(response.json(), value)
                    extract_data = {key: extract_value[0]}
                else:
                    raise Exception("不支持的提取方式")
                YamlUtil.write_extract_yaml(extract_data)

    @staticmethod
    def replace_value(data_info):
        if data_info and isinstance(data_info, dict):
            str_data = json.dumps(data_info)
        else:
            str_data = str(data_info)
        for i in range(str_data.count("${")):
            if "${" in str_data and "}" in str_data:
                start_index = str_data.index("${")
                end_index = str_data.index("}")
                old_value = str_data[start_index:end_index + 1]
                fun_end_inx = old_value.index("(")
                fun_name = old_value[2:fun_end_inx]
                pars = old_value[fun_end_inx + 1:-2].split(",")
                new_value = getattr(DebugTalk(), fun_name)(*pars)
                # new_value = YamlUtil.read_extract_yaml(old_value[2:-1])
                str_data = str_data.replace(old_value, str(new_value))
        if isinstance(data_info, dict):
            new_data = json.loads(str_data)
        else:
            new_data = data_info
        return new_data

    def send_request(self, method, uri, **kwargs):
        method = str(method).lower()
        full_url = RequestUtil.base_url + self.replace_value(uri)
        # 替换请求头中的变量
        # if headers and isinstance(headers, dict):
        #     self.new_headers = self.replace_value(headers)
        for key, value in kwargs.items():
            if key in ["params", "data", "json", "headers"]:
                kwargs[key] = self.replace_value(value)
        response = RequestUtil.sess.request(method=method, url=full_url, **kwargs)
        return response


if __name__ == '__main__':
    data = {"username": "${random_num(11111111111,99999999999)}"}
    RequestUtil.replace_value(data)
