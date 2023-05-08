"""
__project__ = 'holoinsight-ai'
__file_name__ = 'features'
__author__ = 'LuYuan'
__time__ = '2023/4/16 20:52'
__info__ =
"""
from typing import Dict, List

import numpy as np

from common.utils import Utils
from common.constants import Constants


class Features:
    def __init__(self, data_by_day: Dict[str, List[float]], algorithm_type: str):
        self.data_by_day = data_by_day
        self.smoothness = True   # A flag indicating whether the waveform is smooth or not
        self.algorithm_type = algorithm_type

    def run(self):
        self.smoothness = self.waveform_smoothness_checker()
        if self.smoothness:
            features = self.one_diff()
        else:
            features = self.zero_diff()
        return features

    def one_diff(self):
        features_by_duration = {}
        for duration in Constants.WINDOW_LIST.value:
            features_by_duration[str(duration)] = self.do_cutoff(data_by_day=self.data_by_day, duration=duration)
        return features_by_duration

    def zero_diff(self):
        return self.data_by_day  # If the waveform is not smooth, return the raw data

    def do_cutoff(self, data_by_day: Dict[str, List[float]], duration: int) -> Dict[str, List[float]]:
        """
        Use a layering algorithm to determine whether the data should be sliced.

        @param duration: The length of the fixed window to use for slicing.
        @param data_by_day: The data to be analyzed, grouped by day.
        @return: A dictionary of features, grouped by day.
        """
        features = {}
        is_down = True if self.algorithm_type == "down" else False
        for k, v in data_by_day.items():
            features[k] = Utils.diff_percentile_func(v, duration, is_down)
        return features

    def waveform_smoothness_checker(self):
        """
        Evaluate the smoothness of a time series.

        @return: A flag indicating whether the waveform is smooth or not.
        """
        diff_values = []
        for k, v in self.data_by_day.items():
            diff_values += Utils.diff_percentile_func(v, 1)
        diff_values = [abs(value) for value in diff_values]
        if np.percentile(diff_values, 60) < 10:  # todo test 为小流量最好准备！
            return True
        else:
            return False


if __name__ == "__main__":
    pass
