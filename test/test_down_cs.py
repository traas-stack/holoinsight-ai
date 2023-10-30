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


def run_1():
    """
    Generates data for a cold-start scenario,
    tests the cold_start's ability to detect anomalies.

    :return:
    """
    # Set the detection time
    detect_time = 1681711200000
    # Create a stable time series with specified parameters
    ts = TestDataCreator.create_stable_ts(detect_time, 1 * 1440, 60000, 500, 600)
    # Add anomaly value at the detection time
    ts[str(detect_time)] = 0
    # Create the request body with input time series, detection time, and algorithm and rule configurations
    body = {"inputTimeSeries": ts, "intervalTime": 60000,
            "detectTime": detect_time,
            "algorithmConfig": {"algorithmType": "down", "sensitivity": "mid"},
            "ruleConfig": {"defaultDuration": 1, "customChangeRate": 0.1}}
    # Run the main function with the request body and return the result
    result = run_main(body)
    return result


class TestFunction(unittest.TestCase):

    def test(self):
        self.assertEqual(run_1().get("isException"), True)
        pass


if __name__ == "__main__":
    pass
