import os
import unittest
import jsonpath
from requests import request
from Common.handle_logging import log
from Library.Myddt import ddt, data
from Common.handle_config import conf
from Common.handle_excel import HandleExcel
from Common.handle_path import DATA_DIR
from Common.handle_data import HandleSetup


@ddt
class TestAudit(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR, "apicases.xlxs"), "audit")
    cases = excel.read_data()

    @data(*cases)
    def test_audit(self, case):
        # 第一步：准备数据:获取管理员token
        admin_phone = conf.get("test_data", "phone")
        admin_pwd = conf.get("test_data", "pwd")
        admin_member_id, admin_token = HandleSetup.handle_setup(admin_phone, admin_pwd)
        # 2:获取普通用户id和token
        phone = conf.get("test_data", "phone")
        pwd = conf.get("test_data", "pwd")
        member_id, token = HandleSetup.handle_setup(phone, pwd)
        #每次添加一个新项目
        url = conf.get("env", "url") + "/loan/add"
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = token
        data = {"member_id": member_id,
                "title": "木森借钱造大炮",
                "amount": 2000,
                "loan_rate": 12.0,
                "loan_term": 3,
                "loan_date_type": 1,
                "bidding_days": 5}
        # 发送请求，添加项目
        response = request(method="post", url=url, json=data, headers=headers)
        res = response.json()
        # 提取项目的id给审核的用例使用
        loan_id = jsonpath.jsonpath(res, "$..id")[0]
        url = conf.get("env", "url") + case["url"]
        data = eval(case["data"].replace("#loan_id#", str(loan_id)))
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = admin_token
        method = case["method"]
        expected = eval(case["expected"])
        row = case["case_id"] + 1
        # 第二步：调用接口，获取实际结果
        response = request(url=url, method=method, json=data, headers=headers)
        res = response.json()
        # 第三步：断言
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
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
