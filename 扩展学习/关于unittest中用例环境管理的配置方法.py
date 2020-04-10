import unittest


class MyTest(unittest.TestCase):
    def setUp(self):
        """每条用例执行之前都会执行"""
        print("-------1----setup-----------------")
        pass

    def tearDown(self):
        """每条用例执行之后都会执行"""
        print("-------2----teardown------------------------")
        pass

    @classmethod
    def setUpClass(cls):
        """该测试用例类中所有的用例执行之前会执行"""
        print("-------3----setupclass------------------------")
        pass

    @classmethod
    def tearDownClass(cls):
        """该测试用例类中所有的用例执行之后会执行"""
        print("-------4----teardownclass------------------------")
        pass

    def test_01(self):
        print("用例01正在执行")
        self.assertEqual(100, 100)

    def test_02(self):
        print("用例02正在执行")
        self.assertEqual(200, 200)
