"""
__project__ = 'holoinsight-ai'
__file_name__ = 'pipeline'
__author__ = 'LuYuan'
__time__ = '2022/11/7 17:44'
__info__ = pipeLine
"""
import collections

from common.classes import StatusInOut


class DetectPipeLine:
    def __init__(self, status: StatusInOut):
        """
        Initializes the DetectPipeLine object with a given status.

        :param status: The initial status for the pipeline
        """
        self.q = None
        self.status = status

    def start(self, func):
        """
        Initializes the pipeline queue with the given function.

        :param func: The function to be added to the queue
        :return: None
        """
        self.q = collections.deque()
        self.q.append(func)

    def add(self, func):
        """
        Adds a function to the end of the pipeline queue.

        :param func: The function to be added to the queue
        :return: None
        """
        self.q.append(func)

    def handler(self):
        """
        Iterates through the pipeline queue, passing the status object to each function and updating the status object.

        :return: None
        """
        while self.q:
            self.status = self.q[0](self.status)
            self.q.popleft()


if __name__ == "__main__":
    pass
