"""
__project__ = 'holoinsight-ai'
__file_name__ = 'base'
__author__ = 'LuYuan'
__time__ = '2023/4/12 20:45'
__info__ =
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class DetectInfo:
    """
    Information about the sensitive data and algorithm type used for anomaly detection.
    """
    sensitive: str
    algorithm_type: str  # "up"/"down"


@dataclass
class RuleInfo:
    """
    Information about the anomaly detection rules, including minimum duration, thresholds, and change rate.
    """
    min_duration: int
    up_threshold: float
    down_threshold: float
    change_rate: float


@dataclass
class ErrorInfo:
    """
    Information about any errors encountered during the anomaly detection process.
    """
    errorOrNot: bool = False
    msg: str = ''


@dataclass
class Request4AD:
    """
    Request information for time series anomaly detection, including trace ID, data by day, detection info,
    and rule info.
    """
    trace_id: str
    data_by_day: dict
    detect_info: DetectInfo
    rule_info: RuleInfo


@dataclass
class StatusInOut:
    """
    Pipeline status information for anomaly detection.
    """
    alarmOrNot: bool = False  # True indicates current alarm, default is False
    needNext: bool = False  # True indicates no need for next step, default is False
    duration: int = 0  # Default is 0
    passReason: str = ''  # Default is ''
    alarmReason: str = ''  # Default is ''


@dataclass
class Response4AD:
    """
    Results of time series anomaly detection, including whether an anomaly was detected, success status, duration,
    and various metrics.
    """
    isException: bool = False
    success: bool = True  # Whether the detection ran successfully
    duration: int = 0
    alarmCategory: str = ""
    filterReason: str = ""
    alarmMsg: str = ""
    currentValue: float = 0.0
    changeRate: float = 0.0  # # Not percentage format
    extremeValue: float = 0.0
    baseLineValue: float = 0.0
    anomalyData: List[float] = field(default_factory=lambda: [])

    def get_msg(self):
        """
        Returns a dictionary containing the isException and success attributes of the Response4AD object.
        """
        return {"isException": self.isException, "isSuccessful": self.success, "alarmMsg": self.alarmMsg}


if __name__ == "__main__":
    pass
