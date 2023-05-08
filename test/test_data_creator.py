# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__project__ = 'holoinsight-ai'
__file_name__ = 'data_process'
__author__ = 'LuYuan'
__time__ = '2023/4/12 10:50'
__info__ =
"""
import random
import numpy as np
import matplotlib.pyplot as plt

from typing import Dict

from common.utils import Utils


class TestDataCreator:

    @staticmethod
    def create_stable_ts(end_time: int, ts_length: int, period: int, down: int, up: int) -> Dict[str, float]:
        """

        :param up:
        :param down:
        :param end_time:
        :param ts_length:
        :param period: 粒度，此处默认为60000
        :return:
        """
        ts = {}
        start_time = end_time - ts_length * period
        random.seed(0)
        for i in range(start_time, end_time + period, period):  # 确保能够取到detect time
            ts[str(i)] = random.randint(down, up)
        return ts

    @staticmethod
    def create_periodic_ts(end_time: int, ts_length: int, period: int, median_value: int) -> Dict[str, float]:
        """

        :param median_value:
        :param end_time:
        :param ts_length:
        :param period: 粒度，此处默认为60000
        :return:
        """
        days = int(np.ceil(ts_length / 1440))
        start_time = end_time - ts_length * period
        all_ts = []
        for i in range(days):
            time_points = [i * (2 * np.pi / 1440) for i in range(1440)]
            all_ts += [median_value + -int(100 * np.sin(t) + int(100 * random.uniform(-0.1, 0.1))) for t in time_points]
        time_stamps = list(range(start_time + period, end_time + period, period))
        ts = {}
        for i, v in enumerate(time_stamps):
            ts[str(v)] = all_ts[i]
        return ts

    @staticmethod
    def plot(ts, detect_time, period):
        start = min([int(key) for key in ts.keys()])
        ts = Utils().time_series_min_str(ts, start, detect_time + 60000, period)
        plt.plot(ts)
        plt.show()


if __name__ == "__main__":
    ts = TestDataCreator.create_periodic_ts(1681711200000, 3 * 1440 + 1, 60000, 1000)
    TestDataCreator.plot(ts, 1681711200000, 60000)
    pass
