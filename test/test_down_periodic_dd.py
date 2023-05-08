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


def run_2():
    """
    Generates periodic data for a normal scenario,
    tests the data-driven detector's ability to detect anomalies.

    :return:
    """
    detect_time = 1681711200000
    ts = TestDataCreator.create_periodic_ts(end_time=detect_time, ts_length=5 * 1440, period=60000, median_value=1000)
    ts[str(detect_time)] = 500
    body = {"InputTimeSeries": ts, "intervalTime": 60000,
            "detectTime": detect_time,
            "algorithmConfig": {"algorithmType": "down", "sensitivity": "mid"},
            "ruleConfig": {"defaultDuration": 1,
                           "customChangeRate": 0.05}}
    result = run_main(body)
    return result


class TestFunction(unittest.TestCase):

    def test(self):
        self.assertEqual(run_2().get("isException"), True)
        pass


if __name__ == "__main__":
    pass
