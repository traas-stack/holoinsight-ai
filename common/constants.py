"""
__project_ = 'holoinsight-ai'
__file_name__ = 'contants'
__author__ = 'luyuan'
__time__ = '2021-08-09 16:30'
__product_name = PyCharm
__info__:
"""
from enum import Enum
from math import inf


class Constants(Enum):
    """
    A class containing various constants used in the AD system.
    """
    WINDOW_LIST = [1, 3, 5, 7, 9]   # A list of window sizes used in the AD system.
    MIN_DURATION_DEFAULT = 1  # The default minimum duration used in the AD system.
    CUSTOM_UP_THRESHOLD = float(inf)  # The default upper threshold used in the AD system.
    CUSTOM_DOWN_THRESHOLD = -float(inf)  # The default lower threshold used in the AD system.
    CUSTOM_CHANGE_RATE_DEFAULT = 0.05  # The default change rate used in the AD system.
    ALGORITHM_TYPE_UP = "up"  # the algorithm_type up
    ALGORITHM_TYPE_DOWN = "down"  # the algorithm_type down


if __name__ == "__main__":
    pass
