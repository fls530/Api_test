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

filename = os.path.join(DATA_DIR, "apicases.xlsx")


@ddt
class RegisterTestCase(unittest.TestCase):
    excel = HandleExcel(filename, "register")
    cases = excel.read_data()

    @data(*cases)
    def test_register(self, case):
        # 第一步：准备用例数据
        # 请求方法
        method = case["method"]
        # 请求地址
        url = conf.get("env", "url") + "/member/register"
        # 判断是否有手机号需要替换
        if "#phone#" in case["data"]:
            # 随机生成一个手机号码
            phone = self.random_phone()
            # 将参数中的#phone#，替换成随机生成的手机号
            case["data"] = case["data"].replace("#phone#", phone)
        # 请求参数
        data = eval(case["data"])
        # 请求头
        headers = eval(conf.get("env", "headers"))
        # 预期结果
        expected = eval(case["expected"])
        # 用例所在行
        row = case["case_id"] + 1
        # 第二步：发送请求获取实际结果
        response = request(method=method, url=url, json=data, headers=headers)
        # 获取实际结果
        res = response.json()
        print("预期结果：", expected)
        print("实际结果：", res)
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

    @classmethod
    def random_phone(cls):
        """生成一个数据库里面未注册的手机号码"""
        while True:
            phone = "155"
            for i in range(8):
                r = random.randint(0, 9)
                phone += str(r)
            # 数据库查询该手机号是否存在
            sql = "SELECT * FROM futereloan.member WHERE mobile_phone={}".format(phone)
            res = db.find_count(sql)
            # 如果不存在，返回该手机号
            if res == 0:
                return phone
