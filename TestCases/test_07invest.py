import os
import unittest
import random
from Common.handle_excel import HandleExcel
from Library.Myddt import ddt, data
from Common.handle_config import conf
from requests import request
from Common.handle_logging import log
from Common.handle_path import DATA_DIR
from Common.handle_mysql import db
from Common.handle_data import HandleSetup, replace_data
import jsonpath

filename = os.path.join(DATA_DIR, "apicases.xlsx")


@ddt
class TestInvset(unittest.TestCase):
    execl = HandleExcel(filename, "invest")
    cases = execl.read_data()

    @data(*cases)
    def test_invest(self, case):
        """投资用例"""
        # 第一步：准备数据
        url = conf.get("env", "url") + case["url"]
        method = case["method"]
        headers = eval(conf.get("env", "headers"))
        if case["interface"] != "login":
            # 如果不是登陆接口，添加一个token
            headers["Authorization"] = getattr(HandleSetup, "token")
        data = eval(replace_data(case["data"]))
        expected = eval(case["expected"])
        row = case["case_id"] + 1
        response = request(url, method, json=data, headers=headers)
        res = response.json()
        if case["interface"] == "login":
            # 如果是登陆接口，提取id和token
            member_id = str(jsonpath.jsonpath(res, "$..id")[0])
            token = "Bearer" + " " + jsonpath.jsonpath(res, "$..token")[0]
            setattr(HandleSetup, "member_id", member_id)
            setattr(HandleSetup, "token", token)
        if case["interface"] == "add":
            # 如果是加标接口，提取id进行保存
            loan_id = str(jsonpath.jsonpath(res, "$..id")[0])
            setattr(HandleSetup, "loan_id", loan_id)
        # 断言
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["meg"])
        except AssertionError as e:
            # 结果回写excel中
            log.error("用例--{}--执行未通过".format(case["title"]))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            log.exception(e)
            self.excel.write_data(row=row, column=8, value="未通过")
            raise e
        else:
            # 结果回写excel中
            log.info("用例--{}--执行通过".format(case["title"]))
            self.excel.write_data(row=row, column=8, value="通过")
