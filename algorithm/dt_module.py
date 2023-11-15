"""
__project__ = 'holoinsight-ai'
__file_name__ = 'outlier_detector'
__author__ = 'LuYuan'
__time__ = '2023/4/13 15:43'
__info__ =
"""
from algorithm.module import BaseModule
from algorithm.pipeline import DetectPipeLine
from algorithm.dyn_thresh.dyn_thresh_detector import DynamicThresholdDetector
from algorithm.dyn_thresh.rule_checker import RuleChecker
from common.classes import StatusInOut


class DynamicThresholdModule(BaseModule):

    def pipeline(self):
        """
        The core processing pipeline for the DynamicThresholdModule

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
        train_data = {k: v for k, v in self.req.data_by_day.items() if k != "0"}
        rule_result = RuleChecker(detect_data, self.req).detector()
        if rule_result:
            status.alarmOrNot = rule_result
            return status
        dtd = DynamicThresholdDetector(detect_data, train_data, self.req.detect_info.algorithm_type)
        dt = dtd.run()
        if dt:
            status.alarmOrNot = dt
            status.needNext = True
            status.alarmReason = dtd.alarm_info
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
        rre = RuleChecker(detect_data, self.req).filter()
        if rre:
            status.alarmOrNot = False
            status.needNext = False
        return status

    def msg_builder(self, status: StatusInOut) -> StatusInOut:
        """
        Builds the alarm message for the input data

        :param status: The current status object
        :return: The updated status object
        """
        return status

    def to_resp(self, status):
        """
        Returns the final response object based on the input data and the status object

        :param status: The current status object
        :return: The updated status object
        """
        if status.alarmOrNot:
            self.resp.isException = True
            self.resp.alarmMsg = status.alarmReason
        return status


if __name__ == "__main__":
    pass
