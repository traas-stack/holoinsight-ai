"""
__project__ = 'holoinsight-ai'
__file_name__ = 'context_builder'
__author__ = 'LuYuan'
__time__ = '2023/4/12 20:35'
__info__ = build the request
"""
from typing import Dict

from common.classes import DetectInfo, RuleInfo, Request4AD
from common.constants import Constants
from common.utils import Utils


class RequestBuilder:
    def __init__(self, input_body: dict):
        self.body = input_body
        self.req = None

    def build_req(self):
        """
        Builds and returns an AD request object based on the input body.

        @return: The built AD request object.
        """
        # Data processing
        ts = self.body.get("inputTimeSeries")
        detect_time = self.body.get("detectTime")
        period = self.body.get("intervalTime")
        data_by_data = self.data_process(ts, detect_time, period, detect_length=self.period_mapper(period))

        # Detect information
        algorithm_type = self.body.get("algorithmConfig").get("algorithmType")
        detect_info = DetectInfo(sensitive=self.body.get("algorithmConfig").get("sensitivity", "mid"),
                                 algorithm_type=algorithm_type
                                 )

        # Rule information
        if self.body.get("ruleConfig") is None:
            self.body["ruleConfig"] = {}
        up_threshold = Constants.CUSTOM_UP_THRESHOLD.value
        down_threshold = Constants.CUSTOM_DOWN_THRESHOLD.value
        rule_info = RuleInfo(
            min_duration=self.body.get("ruleConfig").get("defaultDuration", Constants.MIN_DURATION_DEFAULT.value),
            up_threshold=self.body.get("ruleConfig").get("customUpThreshold", up_threshold),
            down_threshold=self.body.get("ruleConfig").get("customDownThreshold", down_threshold),
            change_rate=self.body.get("ruleConfig").get("customChangeRate", Constants.CUSTOM_CHANGE_RATE_DEFAULT.value),
        )

        # Build and return the AD request object
        self.req = Request4AD(trace_id=self.body.get("traceId"),
                              data_by_day=data_by_data,
                              detect_info=detect_info,
                              rule_info=rule_info
                              )
        return self.req

    @staticmethod
    def data_process(time_series: Dict[str, float], detect_time: int, period: int, detect_length) -> dict:
        """
        Transforms input test data into a list of tuples representing the time periods that need to be analyzed.

        @param time_series: A dictionary containing the input time series data.
        @param detect_time: The detection time.
        @param period: The period of the input data.
        @param detect_length: The detection length.
        @return: A dictionary containing the processed data grouped by day.
        """
        detect_time += period  # make sure to get the running time
        detect_left_time = detect_time - detect_length * period
        earliest_time = min([int(key) for key in list(time_series.keys())])
        day_num = int((detect_left_time - earliest_time) / (1440 * 60000))
        data_groups = []
        while len(data_groups) < day_num:
            if len(data_groups) == 0:
                data_groups.append((detect_time - detect_length * period, detect_time))
            else:
                cur_start, cur_end = data_groups[-1][0], data_groups[-1][1]
                data_groups.append((cur_start - 1440 * 60000, cur_end - 1440 * 60000))
        data_by_day = {}
        for i, (left, right) in enumerate(data_groups):
            data_by_day[str(i)] = Utils().time_series_min_str(time_series, left, right, period)
        if len(data_groups) == 0:
            data_by_day = {str(0): Utils().time_series_min_str(time_series, earliest_time, detect_time, period)}
        return data_by_day

    @staticmethod
    def period_mapper(period) -> int:
        """
        Maps the period of the input data to the corresponding analysis length.

        @param period: The period of the input data.
        @return: The corresponding analysis length.
        """
        if period == 60000:
            return 24 * 60
        else:
            return 24 * 60


if __name__ == "__main__":
    pass
