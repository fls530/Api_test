from Common.handle_config import conf
from requests import request
import jsonpath
import re


class HandleSetup:
    @staticmethod
    def handle_setup(phone, pwd):
        url = conf.get("env", "url") + "/member/login"
        data = {
            "mobile_phone": phone,
            "pwd": pwd
        }
        headers = eval(conf.get("env", "headers"))
        response = request(method="post", url=url, json=data, headers=headers)
        res = response.json()
        member_id = str(jsonpath.jsonpath(res, "$..id")[0])
        token = "Bearer" + " " + jsonpath.jsonpath(res, "$..token")[0]
        return member_id, token

    @staticmethod
    def handle_case(case, member_id, token):
        url = conf.get("env", "url") + case["url"]
        method = case["method"]
        # 替换参数中的ID
        data = eval(HandleSetup.replace_data(case["data"], member_id))
        # 准备请求头
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = token
        # 发送请求获取实际结果
        response = request(url=url, method=method, json=data, headers=headers)
        res = response.json()
        return data, res


def replace_data(data):
    """替换数据"""
    while re.search("#(.*?)#", data):
        res = re.search("#(.*?)", data)
        key = res.group()
        item = res.group(1)
        try:
            value = conf.get("test_data", item)
        except:
            value = getattr(HandleSetup, item)
        data = data.replace(key, value)
    return data
