"""
__project__ = 'holoinsight-ai'
__file_name__ = 'run_detector'
__author__ = 'LuYuan'
__time__ = '2023/2/1 16:25'
__info__ =
"""
from common.classes import Request4AD
from common.request_builder import RequestBuilder
from handlers.detect_handlers import ColdStartDetectHandler, DynamicThresholdDetectHandler


def run_main(body):
    """
    Runs the detection pipeline on the input request body.

    :param body: A dictionary containing data to be processed
    :return: A string message containing the results of the detection pipeline
    """
    # Builds a request object from the input body
    req = RequestBuilder(body).build_req()
    # Maps the request to the appropriate handler based on the data by day
    target_handler = handler_mapper(req=req)
    # Runs the detection pipeline using the target handler
    resp = target_handler(req).run()
    # Returns the result message from the response
    return resp.get_msg()


def handler_mapper(req: Request4AD):
    """
    Maps the request to the appropriate handler based on the data by day
    """
    if len(req.data_by_day) == 1:
        # Use ColdStartDetectHandler for single-day data
        return ColdStartDetectHandler
    elif len(req.data_by_day) > 1:
        # Use DynamicThresholdDetectHandler for multi-day data
        return DynamicThresholdDetectHandler


if __name__ == "__main__":
    pass
