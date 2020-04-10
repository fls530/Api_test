import os
import unittest
from Library.Myddt import ddt, data
from Common.handle_logging import log
from Common.handle_config import conf
from Common.handle_path import DATA_DIR
from Common.handle_excel import HandleExcel
from Common.handle_data import HandleSetup
from requests import request


@ddt
class TestUpdate(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR, "apicases.xlsx"), "user_info")
    cases = excel.read_data()

    @data(*cases)
    def test_add(self, case):
        # 准备用例数据
        phone = conf.get("test_data", "phone")
        pwd = conf.get("test_data", "pwd")
        member_id, token = HandleSetup.handle_setup(phone, pwd)
        data, res = HandleSetup.handle_case(case, member_id, token)
        row = case["case_id"] + 1
        expected = eval(case["expected"])
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