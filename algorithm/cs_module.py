"""
__project__ = 'holoinsight-ai'
__file_name__ = 'cold_start_algo'
__author__ = 'LuYuan'
__time__ = '2023/4/13 10:19'
__info__ =
"""
from algorithm.module import BaseModule
from algorithm.cold_start.diff_outlier_detector import DiffOutlierDetector
from algorithm.cold_start.rule_checker import RuleChecker
from algorithm.cold_start.similarity_filter import SimilarityFilter
from algorithm.pipeline import DetectPipeLine
from common.classes import StatusInOut


class ColdStartModule(BaseModule):

    def pipeline(self):
        """
        The core processing pipeline for the ColdStartModule

        @return:
        """
        status = StatusInOut()
        try:
            dpp = DetectPipeLine(status)
            dpp.start(self.detector)
            dpp.add(self.filter)
            dpp.add(self.msg_builder)
            dpp.add(self.to_resp)
            dpp.handler()
        except Exception as e:
            self.run_success = False
            self.logger.info(f"traceId: {self.req.trace_id}, runSuccess: {self.run_success}, errorInfo: {e}")
        finally:
            self.logger.info(f"traceId: {self.req.trace_id}, runSuccess: {self.run_success}")

    def detector(self, status: StatusInOut) -> StatusInOut:
        """
        Detects anomalies in the input data and sets the alarmOrNot flag in the status object

        :param status: The current status object
        :return: The updated status object
        """
        detect_data = self.req.data_by_day.get("0")
        rule_result = RuleChecker(detect_data, self.req).detector()
        if rule_result:
            status.alarmOrNot = rule_result
            return status
        p_d_a_d = DiffOutlierDetector(detect_data, self.req.detect_info.algorithm_type)
        re = p_d_a_d.run()
        if re:
            status.alarmOrNot = re
            status.needNext = True
            status.duration = p_d_a_d.real_duration
        return status

    def filter(self, status: StatusInOut) -> StatusInOut:
        """
        Filters out false positives in the input data

        :param status: The current status object
        :return: The updated status object
        """
        if status.needNext is False:
            return status

        detect_data = self.req.data_by_day.get("0")
        sre = SimilarityFilter(detect_data, self.req.detect_info.algorithm_type, status.duration).run()
        rre = RuleChecker(detect_data, self.req).filter(status.duration)
        if sre or rre:
            status.alarmOrNot = False
            status.needNext = False
        return status

    def msg_builder(self, status: StatusInOut) -> StatusInOut:
        """
        Builds the alarm message for the input data

        :param status: The current status object
        :return: The updated status object
        """
        if status.alarmOrNot:
            status.alarmReason = "Cold start alarm!"
        return status

    def to_resp(self, status):
        """
        Returns the final response object based on the input data and the status object

        :param status: The current status object
        :return: The updated status object
        """
        if status.alarmOrNot:
            self.resp.isException = True
        return status


if __name__ == "__main__":
    pass
