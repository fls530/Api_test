import unittest
from Library.Myddt import ddt, data
from Common.handle_excel import HandleExcel
from Common.handle_path import DATA_DIR
import os
from Common.handle_config import conf
from Common.handle_mysql import db
import decimal
from Common.handle_logging import log
from Common.handle_data import HandleSetup


@ddt
class TestRecharge(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR, "apicases.xlsx"), "recharge")
    cases = excel.read_data()

    @data(*cases)
    def test_recharge(self, case):
        # 第一步准备用例参数
        phone = conf.get("test_data", "phone")
        pwd = conf.get("test_data", "pwd")
        member_id, token = HandleSetup.handle_setup(phone, pwd)
        # 判断该用例是否需要数据库校验,获取充值之前的余额
        start_money = TestRecharge.handle_sql(self, case, member_id)
        data, res = HandleSetup.handle_case(case, member_id, token)
        row = case["case_id"] + 1
        expected = eval(case["expected"])
        # 第三步:断言预期结果和实际结果
        try:
            if start_money != 0:
                self.assertEqual(expected["code"], res["code"])
                self.assertEqual(expected["msg"], res["msg"])
                end_money = TestRecharge.handle_sql(self, case, member_id)
                recharge_money = decimal.Decimal(str(data["amount"]))
                self.assertEqual(recharge_money, end_money - start_money)
        except AssertionError as e:
            # 结果回写excel中
            log.error("用例--{}--执行未通过".format(case["title"]))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            log.exception(e)
            self.excel.write_data(row=row, column=8, value="未通过")
            raise e
        else:
            # 通的结果会写到excel
            log.info("用例--{}--执行通过".format(case["title"]))
            self.excel.write_data(row=row, column=8, value="通过")

    def handle_sql(self, case, member_id):
        if case["check_sql"]:
            sql = case["check_sql"].format(member_id)
            money = db.find_one(sql)["leave_amount"]
            return money
        return 0
