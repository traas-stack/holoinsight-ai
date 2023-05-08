"""
__project__ = 'holoinsight-ai'
__file_name__ = 'abnormal_detect'
__author__ = 'LuYuan'
__time__ = '2021-08-09 11:52'
__product_name = PyCharm
__info__: algo module
"""
from abc import ABC

from common.classes import Response4AD, Request4AD, StatusInOut
from common.logger import Logger


class BaseModule(ABC):
    def __init__(self, req: Request4AD):
        """
        Initializes the BaseModule object with a given request object, response object, logger object, and run success flag.

        :param req: The initial request object for the module
        """
        self.run_success = True
        self.req = req
        self.resp = Response4AD()
        self.logger = Logger.get_logger()

    @staticmethod
    def pipeline():
        """The core processing pipeline for the module"""

    @staticmethod
    def filter(status: StatusInOut) -> StatusInOut:
        """Noise filter"""

    @staticmethod
    def detector(status: StatusInOut) -> StatusInOut:
        """Abnormal detector"""

    @staticmethod
    def msg_builder(status: StatusInOut) -> StatusInOut:
        """Alarm information builder"""

    @staticmethod
    def to_resp(status: StatusInOut) -> StatusInOut:
        """Output the result"""


if __name__ == "__main__":
    pass
