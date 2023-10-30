"""
__project__ = 'holoinsight-ai'
__file_name__ = 'test_up'
__author__ = 'LuYuan'
__time__ = '2023/4/17 14:33'
__info__ =
"""
import unittest

from handlers.run_main import run_main
from test.test_data_creator import TestDataCreator


def run_4():
    """
    Generates data for a cold-start scenario,
    tests the cold_start's ability to detect anomalies.

    :return:
    """
    detect_time = 1681711200000
    ts = TestDataCreator.create_stable_ts(detect_time, 1 * 1440, 60000, 500, 600)
    ts[str(detect_time)] = 1000
    body = {"inputTimeSeries": ts, "intervalTime": 60000,
            "detectTime": detect_time,
            "algorithmConfig": {"algorithmType": "up", "sensitivity": "mid"},
            "ruleConfig": {"defaultDuration": 1,
                           "customChangeRate": 0.1}}
    result = run_main(body)
    return result


# class TestFunction(unittest.TestCase):
#
#     def test(self):
#         self.assertEqual(run_4().get("isException"), True)
#         pass


if __name__ == "__main__":
    run_4()
    pass
