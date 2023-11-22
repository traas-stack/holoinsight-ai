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
        ##
        self.alarm_info = ''

    def detector(self):
        """
        Excessive alarm detection

        :return: Boolean indicating if the data exceeds the threshold
        """
        if self.algorithm_type == Constants.ALGORITHM_TYPE_UP.value:
            if self.detect_data[-1] > self.up:
                self.alarm_info = f"The current value {round(abs(self.detect_data[-1]), 2)} " \
                                  f"exceeds the alert baseline {round(abs(self.up), 2)}"
                return True
        elif self.algorithm_type == Constants.ALGORITHM_TYPE_DOWN.value:
            if self.detect_data[-1] < self.down:
                self.alarm_info = f"The current value {round(abs(self.detect_data[-1]), 2)} " \
                                  f"exceeds the alert baseline {round(abs(self.down), 2)}"
                return True
        return False

    def filter(self, duration):
        """
        Rule filtering

        :return: Boolean indicating if the data violates the rules
        """
        custom_change_rate = self.req.rule_info.change_rate
        post = self.detect_data[-duration:]
        pre = self.detect_data[-2 * duration: - duration]
        if self.algorithm_type == "down":
            real_change_rate = 1.0 if max(pre) == 0 else -(min(post) - max(pre)) / max(pre)
        else:
            real_change_rate = 1.0 if np.percentile(pre, 90) == 0 else (max(post) - np.percentile(pre, 90)) \
                                                                       / np.percentile(pre, 90)
        if custom_change_rate > real_change_rate:
            return True
        if self.algorithm_type == Constants.ALGORITHM_TYPE_UP.value and self.detect_data[-1] < self.down:
            return True
        elif self.algorithm_type == Constants.ALGORITHM_TYPE_DOWN.value and self.detect_data[-1] > self.up:
            return True
        return False


if __name__ == "__main__":
    pass
