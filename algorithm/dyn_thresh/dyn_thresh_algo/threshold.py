"""
__project__ = 'holoinsight-ai'
__file_name__ = 'threshold'
__author__ = 'LuYuan'
__time__ = '2023/4/16 19:27'
__info__ =
"""
from typing import List, Dict

import pandas as pd
import numpy as np

from algorithm.dyn_thresh.dyn_thresh_algo.events import PeriodicEventDetector
from algorithm.dyn_thresh.dyn_thresh_algo.node import Node
from common.utils import Utils


class ThresholdCalc:
    def __init__(self, data_by_day: Dict[str, List[float]], boundary=1440):
        self.data_by_day = data_by_day
        # Initialization
        self.boundary = boundary  # Maximum number of data points in a day
        self.steps = 50   # Number of steps to use when calculating threshold values
        self.init_per = 90  # Initial percentile to use when calculating threshold values
        self.similar_index = 1  # Controls the similarity of the threshold values at different levels of the tree
        self.cont_len = 120  # Length of continuous time intervals to break when doing threshold searching

    def run(self):
        df = pd.DataFrame.from_dict(self.data_by_day, orient="index")
        period = self.pp_detect(list(df.min()))  # Detect the periodicity of the data
        if period != -1:
            self.cont_len = int(self.boundary / period / 2)
        dt = PeriodicEventDetector(data_by_day=self.data_by_day,
                                   steps=self.steps,
                                   init_per=self.init_per,
                                   similar_index=self.similar_index,
                                   cont_len=self.cont_len
                                   )
        node_events = dt.run()   # Detect periodic events in the data
        intervals_with_th = self.slice_th_creator(node_events, dt.th_list)
        return self.regression(df, intervals_with_th[-1])

    def slice_th_creator(self, node_events: List[Node], th_list: List[float]):
        """
        Create intervals and their corresponding threshold values.

        @param node_events: A list of periodic event nodes.
        @param th_list: A list of threshold values.
        @return: A list of tuples containing each interval and its corresponding threshold value.
        """
        index_stack = []
        start = 0
        max_level = 0
        for n in node_events:
            max_level = max(n.level, max_level)
            if n.left > start:
                index_stack.append((start, n.left - 1))
            index_stack.append((n.left, n.right))
            start = n.right + 1
        if start < self.boundary:
            index_stack.append((start, self.boundary - 1))
        out_put = []
        if len(th_list) == 1:  # Handle extreme cases
            out_put.append((index_stack[0][0], index_stack[-1][-1], th_list[-1], None))
            return out_put
        for ll, rr in index_stack:
            cur_th = th_list[max_level]
            node = None
            for nn in node_events:
                if nn.matches_interval(ll, rr):
                    node = nn
                    cur_th = min(th_list[nn.drill_down_to_node(0).level], th_list[nn.drill_down_to_node(-1).level])
                    continue
            out_put.append((ll, rr, cur_th, node))
        return out_put

    @staticmethod
    def regression(df, interval_with_th):
        """
        Calculate the target threshold using regression.

        @param df: A pandas dataframe.
        @param interval_with_th: A tuple containing an interval and its corresponding threshold value.
        @return: The target threshold value.
        """
        ll, rr = interval_with_th[0], interval_with_th[1]
        target_th = df.iloc[:, ll:rr + 1].min().min()
        return target_th

    @staticmethod
    def pp_detect(envelope, min_win=140, min_period_interval=15):
        """
         Detect whether the data has a periodic pattern using FFT.

         @param envelope: A list of data points.
         @param min_win: The minimum window size to use when calculating FFT.
         @param min_period_interval: The minimum interval between periodic patterns.
         @return: The number of data points per period, or -1 if no periodic pattern is detected.
         """
        fft_values = np.fft.fft(envelope)
        freq = [abs(v) for v in fft_values[:len(envelope) // 2]]
        search_range = range(int(len(envelope) / min_win), int(len(envelope) / min_period_interval))
        up_threshold = Utils.turkey_box_plot([freq[k] for k in search_range])[4]
        up_threshold = max(1 / 3 * max([freq[k] for k in search_range]), up_threshold)
        index_in = []
        for i, v in enumerate(freq):
            if v > up_threshold and i in search_range:
                index_in.append(i)
        potential_index = []
        for v in index_in:
            if v != max(index_in) and max(index_in) % v == 0:
                potential_index.append(v)
        if len(potential_index) > 0:
            return min(potential_index)
        return -1


if __name__ == "__main__":
    pass
