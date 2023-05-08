"""
__project__ = 'holoinsight-ai'
__file_name__ = 'utils'
__author__ = 'LuYuan'
__time__ = '2023/4/11 17:38'
__info__ = the utils
"""
import math
import numpy as np

from numpy import nan
from typing import List, Dict, Callable, Any


class Utils:

    def diff_feature_calc(self, input_data: List[float], search_length: int) -> list:
        """
        Calculates the difference feature for a given input list.

        :param input_data: A list of floats with length greater than search_length.
        :param search_length: The maximum range for which to calculate the difference feature.
        :return: A list of floats representing the difference feature.
        """
        diff = []
        for i in range(len(input_data) - 1, search_length - 1, -1):
            if input_data[i] - input_data[i - 1] < 0:
                search_list = input_data[i - search_length: i + 1]
                duration = self.monotonic_duration(search_list, True)
                diff.append(input_data[i] - input_data[i - duration + 1])
            else:
                search_list = input_data[i - search_length: i + 1]
                duration = self.monotonic_duration(search_list)
                diff.append(input_data[i] - input_data[i - duration + 1])
        diff.reverse()
        out_put_diffs = search_length * [0] + diff
        return out_put_diffs

    @staticmethod
    def monotonic_duration(lst: List[float], reverse=False):
        """
        Calculates the duration of a monotonic sequence in a given list.

        :param lst: A list of floats.
        :param reverse: If True, treats the list as reversed for calculation.
        :return: An integer representing the duration of the monotonic sequence.
        """
        if reverse:
            lst = [-v for v in lst]
        if len(lst) == 0:
            return 0
        if len(lst) == 1:
            return 1
        count = 1
        for i in range(len(lst) - 1, 0, -1):
            if lst[i] > lst[i - 1]:
                count += 1
            else:
                break
        return count

    @staticmethod
    def turkey_box_plot(input_data: List[float], delta=1.5) -> list:
        """
        Calculates the Tukey box plot for a given input list.

        :param input_data: A list of floats.
        :param delta: The delta value to use for the box plot calculation.
        :return: A list of floats representing the Tukey box plot.
        """
        q1 = np.percentile(input_data, 25)
        q3 = np.percentile(input_data, 75)
        q2 = np.percentile(input_data, 50)
        iqr = q3 - q1
        return [q1, q2, q3, q1 - delta * iqr, q3 + delta * iqr]

    def time_series_min_str(self, p_data: Dict[str, float], start: int, end: int, period: int) -> list:
        """
        Generates a complete minute-level time series.

        @param p_data: A dictionary with index as key and amplitude as value.
        @param start: The start time of the time series in milliseconds.
        @param end: The end time of the time series in milliseconds.
        @param period: The period of each time step in milliseconds.
        @return: A list representing the complete time series.
        """
        out_time_series = []
        for i_time in range(start, end, period):
            if str(i_time) in p_data.keys():
                out_time_series.append(p_data[str(i_time)])
            else:
                out_time_series.append(None)
        out_time_series = self.time_series_imputation(out_time_series)
        return out_time_series

    @staticmethod
    def time_series_imputation(input_data: List[float]) -> list:
        """
         Imputes missing values in a time series.

         @param input_data: A list of floats representing the time series.
         @return: A list of floats with imputed missing values.
         """
        if None in input_data:
            if input_data.count(None) == len(input_data):
                return []
            if input_data[0] is None:
                input_data[0] = next(item for item in input_data if item is not None)
            for i in range(1, len(input_data)):
                if input_data[i] is None or math.isnan(input_data[i]):
                    input_data[i] = input_data[i - 1]
        return input_data

    @staticmethod
    def agg_diff_fe_calc(input_data: List[float], agg_length: int) -> list:
        """
        Calculates aggregated difference features for a given input list.

        @param input_data: A list of floats representing the input data.
        @param agg_length: The length of the aggregation window.
        @return: A list of floats representing the aggregated difference features.
        """
        diff_func: Callable[[Any, Any], None] = lambda a, b: np.sum(a) - np.sum(b)
        diff = []
        for i in range(len(input_data) - 2 * agg_length + 1):
            post = input_data[i + agg_length:i + 2 * agg_length]
            pre = input_data[i:i + agg_length]
            diff.append(diff_func(post, pre))
        return diff

    @staticmethod
    def longest_continuous(lst, target) -> int:
        """
        Finds the length of the longest continuous sequence in a list that meets a given target condition.

        @param lst: A list of values to search.
        @param target: The target value to search for.
        @return: The length of the longest continuous sequence that meets the target condition.
        """
        count = 0
        max_count = 0
        for num in lst:
            if num <= target:
                count += 1
                max_count = max(max_count, count)
            else:
                count = 0
        return max_count

    @staticmethod
    def diff_percentile_func(data: list, step: int, is_down=True) -> list:
        """
        Calculates the percentile difference for a given data list and step size.

        @param data: A list of data values.
        @param step: The step size for calculating the percentile difference.
        @param is_down: A boolean indicating whether the percentile difference should be negative.
        @return: A list of percentile differences.
        """
        diff_list = []
        for i in range(2 * step, len(data)):
            if step == 1:
                if data[i - step] != 0:
                    v = 100 * (data[i] - data[i - step]) / data[i - step]
                    if is_down:
                        diff_list.append(v if v < 0 else 0)
                    else:
                        diff_list.append(-v if v > 0 else 0)
                else:
                    diff_list.append(nan)
            else:
                j = i + 1
                if np.mean(data[j - 2 * step: j - step]) != 0:
                    v = 100 * (np.mean(data[j - step:j]) - np.mean(data[j - 2 * step: j - step])) / np.mean(
                        data[j - 2 * step: j - step])
                    if is_down:
                        diff_list.append(v if v < 0 else 0)
                    else:
                        diff_list.append(-v if v > 0 else 0)
                else:
                    diff_list.append(nan)
        diff_array = np.array(diff_list)
        if diff_array.size - np.isnan(diff_array).sum() == 0:
            fill_value = -100
        else:
            fill_value = np.nanmean(diff_array)
        np.nan_to_num(diff_array, nan=fill_value, copy=False)
        diff_list = diff_array.tolist()
        return (2 * step) * [diff_list[0]] + diff_list


if __name__ == "__main__":
    pass
