"""
__project__ = 'holoinsight-ai'
__file_name__ = 'outlier_detector'
__author__ = 'LuYuan'
__time__ = '2023/4/13 15:43'
__info__ =
"""
from typing import List

from common.constants import Constants
from common.utils import Utils

RATE = 2


class SimilarityFilter:
    def __init__(self, detect_data: List[float], algorithm_type: str, anomaly_duration: int):
        self.algorithm_type = algorithm_type
        self.detect_data = self.minus_data(detect_data)
        self.anomaly_duration = anomaly_duration

    def run(self):
        """
        Check if the current data is similar to the historical data.

        :return: True if the current data is similar to the historical data.
        """
        agg_list = Utils.agg_diff_fe_calc(self.detect_data, self.anomaly_duration)
        if agg_list[-1] < RATE * min(agg_list[:-self.anomaly_duration]):
            return False
        return True

    def minus_data(self, input_data: List[float]) -> List[float]:
        """
        If the algorithm is "up", invert the input data.

        :param input_data: List of input data.
        :return: List of input data with inverted values if the algorithm is "up".
        """
        if self.algorithm_type == Constants.ALGORITHM_TYPE_UP.value:
            return [-value for value in input_data]
        return input_data


if __name__ == "__main__":
    pass
