"""
__project__ = 'holoinsight-ai'
__file_name__ = 'test'
__author__ = 'LuYuan'
__time__ = '2023/4/18 11:56'
__info__ =
"""
import unittest

from test.test_down_cs import run_1
from test.test_down_cs_noise import run_8
from test.test_down_periodic_dd import run_2
from test.test_down_stable_dd import run_3
from test.test_up_cs import run_4
from test.test_up_cs_noise import run_9
from test.test_up_periodic_dd import run_5
from test.test_up_stable_dd import run_6
from test.test_up_stable_dd_noise import run_7


class TestFunction(unittest.TestCase):
    """
    All test cases.
    """

    def test1(self):
        self.assertEqual(run_1().get("isException"), True)
        pass

    def test2(self):
        self.assertEqual(run_2().get("isException"), True)
        pass

    def test3(self):
        self.assertEqual(run_3().get("isException"), True)
        pass

    def test4(self):
        self.assertEqual(run_4().get("isException"), True)
        pass

    def test5(self):
        self.assertEqual(run_5().get("isException"), True)
        pass

    def test6(self):
        self.assertEqual(run_6().get("isException"), True)
        pass

    def test7(self):
        self.assertEqual(run_7().get("isException"), False)
        pass

    def test8(self):
        self.assertEqual(run_8().get("isException"), False)
        pass

    def test9(self):
        self.assertEqual(run_9().get("isException"), False)
        pass


if __name__ == "__main__":
    pass
