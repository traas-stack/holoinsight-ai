"""
__project__ = 'holoinsight-ai'
__file_name__ = 'rule_filter'
__author__ = 'LuYuan'
__time__ = '2023/4/14 10:14'
__info__ =
"""
import numpy as np

from typing import List
from common.classes import Request4AD
from common.constants import Constants


class RuleChecker:
    def __init__(self, detect_data: List[float], req: Request4AD):
        self.req = req
        self.detect_data = detect_data
        self.up = self.req.rule_info.up_threshold
        self.down = self.req.rule_info.down_threshold
        self.algorithm_type = self.req.detect_info.algorithm_type

    def detector(self):
        """
        Excessive alarm detection

        :return: Boolean indicating if the data exceeds the threshold
        """
        if self.algorithm_type == Constants.ALGORITHM_TYPE_UP.value:
            if self.detect_data[-1] > self.up:
                return True
        elif self.algorithm_type == Constants.ALGORITHM_TYPE_DOWN.value:
            if self.detect_data[-1] < self.down:
                return True
        return False

    def filter(self):
        """
        Rule filtering

        :return: Boolean indicating if the data violates the rules
        """
        if self.algorithm_type == Constants.ALGORITHM_TYPE_UP.value and self.detect_data[-1] < self.down:
            return True
        elif self.algorithm_type == Constants.ALGORITHM_TYPE_DOWN.value and self.detect_data[-1] > self.up:
            return True

        custom_change_rate = self.req.rule_info.change_rate
        train_data = {k: v for k, v in self.req.data_by_day.items() if k != "0"}
        compare_values = []
        for k, v in train_data.items():
            compare_values.append(v[-1])
        baseline = np.max(compare_values)
        if baseline == 0:
            return True
        if self.algorithm_type == "down":
            if custom_change_rate > -(self.detect_data[-1] - baseline) / baseline:
                return True
        else:
            if custom_change_rate > (self.detect_data[-1] - baseline) / baseline:
                return True
        return False


if __name__ == "__main__":
    pass
