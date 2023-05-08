"""
__project_ = 'holoinsight-ai'
__file_name__ = 'handler base'
__author__ = 'LuYuan'
__time__ = '2021-08-09 14:02'
__product_name = PyCharm
__info__: handler
"""
from abc import ABC

from algorithm.cs_module import ColdStartModule
from algorithm.dt_module import DynamicThresholdModule
from common.classes import Request4AD, Response4AD


class BaseHandler(ABC):
    def __init__(self, req: Request4AD):
        """
        Initializes the BaseHandler with a request object and sets the run_success attribute to True.

        :param req: A Request4AD object containing data to be processed.
        """
        self.req = req
        self.run_success = True

    @staticmethod
    def run(self):
        """
        Runs the detection pipeline.
        This method is abstract and must be implemented by child classes.
        """


class ColdStartDetectHandler(BaseHandler):
    """
    Handles detection of a single dimension value increase.
    """
    def run(self) -> Response4AD:
        """
        Runs the ColdStartModule pipeline and returns the result.

        :return: A Response4AD object containing the result of the pipeline.
        """
        cs = ColdStartModule(self.req)
        cs.pipeline()
        return cs.resp


class DynamicThresholdDetectHandler(BaseHandler):
    """
    Handles detection of a single dimension value decrease.
    """
    def run(self) -> Response4AD:
        """
        Runs the DataDrivenModule pipeline and returns the result.

        :return: A Response4AD object containing the result of the pipeline.
        """
        dd = DynamicThresholdModule(self.req)
        dd.pipeline()
        return dd.resp


if __name__ == "__main__":
    pass
