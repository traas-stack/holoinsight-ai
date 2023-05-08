"""
__project_ = 'holoinsight-ai'
__file_name__ = 'common_logger'
__author__ = 'luyuan'
__time__ = '2021-12-15 22:24'
__product_name = PyCharm
__info__:
"""
import logging


class Logger(object):
    def __init__(self):
        super()

    @staticmethod
    def get_logger():
        logging.basicConfig(level=logging.INFO)
        return logging


if __name__ == "__main__":
    pass
