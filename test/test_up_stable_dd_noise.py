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


def run_7():
    """
    Generates stable data for a normal scenario,
    tests the data-driven detector's ability to filter the noise.

    :return:
    """
    detect_time = 1681711200000
    ts = TestDataCreator.create_stable_ts(end_time=detect_time, ts_length=5 * 1440, period=60000, down=500, up=600)
    # Add values at specific times to create a periodic noise
    ts[str(detect_time)] = 1000
    ts[str(detect_time - 1440 * 60000)] = 1000
    ts[str(detect_time - 2 * 1440 * 60000)] = 1000
    ts[str(detect_time - 3 * 1440 * 60000)] = 1000
    ts[str(detect_time - 4 * 1440 * 60000)] = 1000
    body = {"InputTimeSeries": ts, "intervalTime": 60000,
            "detectTime": detect_time,
            "algorithmConfig": {"algorithmType": "up", "sensitivity": "mid"},
            "ruleConfig": {"defaultDuration": 1,
                           "customChangeRate": 0.1}
            }
    result = run_main(body)
    return result


class TestFunction(unittest.TestCase):

    def test(self):
        self.assertEqual(run_7().get("isException"), False)
        pass


if __name__ == "__main__":
    pass
