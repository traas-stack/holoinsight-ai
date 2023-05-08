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


def run_8():
    """
    Generates data for a cold-start scenario,
    tests the similarity filter's ability to filter the noise.

    :return:
    """
    detect_time = 1681711200000
    ts = TestDataCreator.create_stable_ts(detect_time, 1 * 1440, 60000, 500, 600)
    # Add anomaly value at the detection time and a value 500 intervals before the detection time
    ts[str(detect_time)] = 0
    ts[str(detect_time - 500 * 60000)] = 0
    body = {"InputTimeSeries": ts, "intervalTime": 60000,
            "detectTime": detect_time,
            "algorithmConfig": {"algorithmType": "down", "sensitivity": "mid"},
            "ruleConfig": {"defaultDuration": 1, "customChangeRate": 0.1}}
    result = run_main(body)
    return result


class TestFunction(unittest.TestCase):

    def test(self):
        self.assertEqual(run_8().get("isException"), False)
        pass


if __name__ == "__main__":
    pass
