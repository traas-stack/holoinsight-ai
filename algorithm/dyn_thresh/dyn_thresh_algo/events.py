"""
__project__ = 'holoinsight-ai'
__file_name__ = 'DynamicThreshold'
__author__ = 'LuYuan'
__time__ = '2023/4/11 17:37'
__info__ =
"""
import numpy as np
import pandas as pd

from typing import Dict, List
from pandas import DataFrame

from algorithm.dyn_thresh.dyn_thresh_algo.node import Node
from common.utils import Utils

NEIGHBOR = 30
THRESHOLD_LEVEL_RATE = 0.2


class PeriodicEventDetector:
    def __init__(self, data_by_day: Dict[str, List[float]], steps: int, init_per: float, similar_index: int,
                 cont_len: int):
        self.dod_data = data_by_day
        self.history_keys = list(self.dod_data.keys())
        self.data_len = None
        self.steps = steps
        self.init_per = init_per
        self.similar_index = similar_index
        self.cont_len = cont_len
        #
        self.neighbor = NEIGHBOR
        self.threshold_level_rate = THRESHOLD_LEVEL_RATE
        # out_put
        self.th_list = []

    def run(self):
        df = pd.DataFrame.from_dict(self.dod_data, orient="index")
        self.data_len = df.shape[1]
        min_value, max_value = np.percentile(df.values, 0), np.percentile(df.values, self.init_per)
        if min_value == max_value:
            self.th_list = [min_value]
            return [Node(level=-1, left=0, right=self.data_len - 1)]
        th_list = [min_value - i * (min_value - max_value) / self.steps for i in range(self.steps)]
        self.th_list = th_list
        events = self.find_periodic_events(df, th_list)
        return events

    def find_periodic_events(self, df: DataFrame, th_list: List[float]) -> List[float]:
        """
        Identify periodic events.

        @param df: The raw data.
        @param th_list: A list of threshold values to use for slicing the data.
        @return: A list of periodic events.
        """
        pre_level_nodes = []
        for i, cur_th in enumerate(th_list):
            raw_nodes = self.raw_nodes_search(df, cur_th, i)
            if len(raw_nodes) == 0:
                continue
            raw_nodes_with_parents = self.node_parents_update(raw_nodes, pre_level_nodes)
            cur_level_nodes = []
            for r_node in raw_nodes_with_parents:
                if not r_node.parents:
                    cur_level_nodes.append(r_node)
                elif len(r_node.parents) == 1:
                    mid_left_nodes = self.modify_node_boundary(r_node, 0)
                    mid_right_nodes = self.modify_node_boundary(mid_left_nodes[-1], -1)
                    if len(mid_left_nodes) == 1:
                        nodes_with_processed = mid_right_nodes
                    else:
                        nodes_with_processed = [mid_left_nodes[0]] + mid_right_nodes
                    cur_level_nodes += nodes_with_processed
                elif len(r_node.parents) > 1:
                    processed_node_cluster = self.nodes_process(r_node, self.node_cluster(r_node.parents))
                    cur_level_nodes += processed_node_cluster
            pre_level_nodes = cur_level_nodes
        return pre_level_nodes

    def raw_nodes_search(self, df: DataFrame, cur_th: float, level: int) -> List[Node]:
        """
        Obtain raw nodes by dividing the data according to the specified threshold.

        @param df: The raw data.
        @param cur_th: The current threshold.
        @param level: The current level of the tree.
        @return: A list of raw nodes.
        """
        outlier_list = (df < cur_th).sum(axis=0)
        duration = Utils.longest_continuous(outlier_list.tolist(), 0)
        if duration < self.cont_len:
            return []
        raw_nodes = self.get_raw_nodes(outlier_list=outlier_list.tolist(),
                                       count=max(1, int(len(self.history_keys) / self.similar_index)),
                                       level=level,
                                       neighbor=self.neighbor)
        return raw_nodes

    def nodes_process(self, completed_node: Node, node_clu_list: List[List[Node]]) -> List[Node]:
        """
        Split/merge nodes with multiple parents; split the two sides of the overall node!
        Splitting scenario: for example, when two parents are very large in size.

        @param completed_node: The entire Node after a split.
        @param node_clu_list: Clustering of parents corresponding to the overall node according to certain rules.
        @return: A list of processed nodes.
        """
        processed_node_cluster = []
        for n_list in node_clu_list:
            processed_node_cluster += self.node_process_within_group(n_list)
        processed_node_cluster = self.node_process_between_group(processed_node_cluster)
        if completed_node.left != processed_node_cluster[0].left:
            new_nodes = self.modify_node_boundary(
                Node(level=completed_node.level, left=completed_node.left, right=processed_node_cluster[0].right,
                     parents=[processed_node_cluster[0]]), 0)
            processed_node_cluster = new_nodes + processed_node_cluster[1:]
        else:
            copy_node = processed_node_cluster[0].copy_node()
            copy_node.parents = [processed_node_cluster[0]]
            processed_node_cluster[0] = copy_node
        if completed_node.right != processed_node_cluster[-1].right:
            new_nodes = self.modify_node_boundary(
                Node(level=completed_node.level, left=processed_node_cluster[-1].left, right=completed_node.right,
                     parents=[processed_node_cluster[-1]]), -1)
            processed_node_cluster = processed_node_cluster[:-1] + new_nodes
        else:
            copy_node = processed_node_cluster[-1].copy_node()
            copy_node.parents = [processed_node_cluster[-1]]
            processed_node_cluster[-1] = copy_node
        for p_n in processed_node_cluster:
            p_n.level = completed_node.level
        return processed_node_cluster

    def node_process_within_group(self, node_list: List[Node]) -> List[Node]:
        """
        The input is a clustered list of nodes with levels within a certain range,
        arranged from left to right by default.

        @param node_list: A list of nodes with the same parent.
        @return: A list of processed nodes.
        """
        new_node_list = [node_list[0]]  # todo
        for node in node_list[1:]:
            l1, l2 = new_node_list[-1].drill_down_to_node(-1).level, node.drill_down_to_node(0).level
            pre_r_index, post_l_index = new_node_list[-1].right, node.left
            if post_l_index - pre_r_index > 1:
                if node.level - max(l1, l2) < int(self.threshold_level_rate * self.steps):
                    new_node_list[-1] = self.node_merge(new_node_list[-1], node)
                else:
                    mid_node = Node(level=node.level, left=pre_r_index + 1, right=post_l_index - 1)
                    if l1 > l2:
                        new_node_list[-1] = self.node_merge(new_node_list[-1], mid_node)
                        new_node_list.append(node)
                    else:
                        new_node_list.append(self.node_merge(mid_node, node))
            else:
                new_node_list[-1] = self.node_merge(new_node_list[-1], node)
        return new_node_list

    @staticmethod
    def node_process_between_group(node_list: List[Node]) -> List[Node]:
        """
        The input is a list of processed nodes between clustered groups,
        arranged from left to right by default.

        @param node_list: A list of nodes with the same parent.
        @return: A list of processed nodes.
        """
        new_node_list = [node_list[0]]
        for node in node_list[1:]:
            pre_r_index, post_l_index = new_node_list[-1].right, node.left
            if post_l_index - pre_r_index > 1:
                mid_node = Node(level=node.level, left=pre_r_index + 1, right=post_l_index - 1)
                new_node_list.append(mid_node)
                new_node_list.append(node)
            else:
                new_node_list.append(node)
        return new_node_list

    def modify_node_boundary(self, node: Node, pos: int) -> List[Node]:
        """
        Boundary processing.

        @param node: The node to be modified.
        @param pos: If pos=0, modify the left boundary; if pos=-1, modify the right boundary.
        @return: A list of modified nodes.
        """
        if not node.parents:
            return [node]
        if node.level - node.drill_down_to_node(pos).level < int(self.threshold_level_rate * self.steps):
            return [node]

        if pos == 0:
            if node.left == node.parents[0].left:
                return [node]
            else:
                ts = node.drill_down_to_level(pos)
                ts.reverse()
                if self.change_point_detect(ts, pos):
                    new_node_list = [
                        Node(level=node.level, left=node.left, right=node.parents[0].left - 1)]
                    node.left = node.parents[0].left
                    new_node_list.append(node)
                    return new_node_list
        elif pos == -1:
            if node.right == node.parents[-1].right:
                return [node]
            else:
                ts = node.drill_down_to_level(pos)
                ts.reverse()
                if self.change_point_detect(ts, pos):
                    new_node_list = [
                        Node(level=node.level, left=node.left, right=node.parents[-1].right,
                             parents=node.parents),
                        Node(level=node.level, left=node.parents[-1].right + 1, right=node.right)]
                    return new_node_list
        return [node]

    def get_raw_nodes(self, level: int, outlier_list: List[int], count: int, neighbor: int) -> List[Node]:
        """
        Select potential event nodes based on specific conditions.

        @param level: The current level.
        @param outlier_list: The list of outlier points.
        @param count: Condition 1.
        @param neighbor: Condition 2.
        @return: A list of potential event nodes.
        """
        event_clusters = self.event_cluster(outlier_list, count, neighbor)
        if len(event_clusters) == 0:
            return []
        node_list = []
        for clu in event_clusters:
            node_list.append(Node(level=level, left=clu[0][0], right=clu[-1][0]))  # 初始parents为空
        return node_list

    @staticmethod
    def node_parents_update(raw_nodes: List[Node], pre_level_nodes: List[Node]) -> List[Node]:
        """
        Find the parents of each raw_node.

        @param raw_nodes: A list of raw nodes.
        @param pre_level_nodes: A list of nodes from the previous level.
        @return: A list of nodes with updated parent information.
        """
        for en in raw_nodes:
            for f_en in pre_level_nodes:
                en.add_parent(f_en)
        return raw_nodes

    @staticmethod
    def node_merge(pre_node: Node, post_node: Node) -> Node:
        """
        Merge two nodes in order.

        @param pre_node: The previous node.
        @param post_node: The next node.
        @return: The merged node.
        """
        node = Node(level=None, left=pre_node.left, right=post_node.right,
                    parents=[pre_node, post_node])
        return node

    @staticmethod
    def node_cluster(lst: List[Node]) -> List[List[Node]]:
        """
        Cluster the nodes, preserving the original level.

        @param lst: A list of nodes.
        @return: A list of clustered nodes.
        """
        if not lst:
            return []
        result = []
        i = 0
        while i < len(lst):
            j = i
            while j < len(lst) - 1 and abs(
                    lst[i].drill_down_to_node(-1).level - lst[j + 1].drill_down_to_node(0).level) < 10:
                j += 1
            result.append(lst[i:j + 1])  # todo 父节点
            i = j + 1
        return result

    @staticmethod
    def change_point_detect(ts, pos) -> bool:
        """
        Find the change point!

        @param pos: The position to check for a change point.
        @param ts: The time series data.
        @return: True if there is a change point at the specified position, False otherwise.
        """
        for i in range(1, 3, 1):
            diffs = Utils().diff_feature_calc(ts, i)
            if pos == 0:
                down_threshold = Utils.turkey_box_plot(diffs[:-1], 2)[3]
                if diffs[-1] < down_threshold and diffs[-1] < min(diffs[:-1]):
                    return True
            elif pos == -1:
                up_threshold = Utils.turkey_box_plot(diffs[:-1], 2)[4]
                if diffs[-1] > up_threshold and diffs[-1] > max(diffs[:-1]):
                    return True
        return False

    @staticmethod
    def event_cluster(lst, count: int, interval):
        """
        Cluster events!

        @param lst: The list of events to cluster.
        @param count: The maximum number of clusters to create.
        @param interval: The time interval to use for clustering.
        @return: The clustered events as a list of lists.
        """
        clu = []
        current_cluster = []
        i = 0
        while i < len(lst):
            if len(current_cluster) == 0:
                if lst[i] >= count:  # fixme
                    current_cluster.append((i, lst[i]))
            else:
                start_loc = current_cluster[-1][0] + 1
                end_loc = min(start_loc + interval, len(lst))
                slice_lst = lst[start_loc:end_loc]
                slice_idx = [start_loc + j for j in range(len(slice_lst)) if slice_lst[j] >= count]
                if slice_idx:
                    current_cluster += [(k, lst[k]) for k in slice_idx]
                else:
                    clu.append(current_cluster)
                    current_cluster = []
                    i = end_loc - 1
            i += 1
        if current_cluster:
            clu.append(current_cluster)
        return clu

    def set_neighbor_len(self, neighbor):
        """
        Set the length of the neighbor list.

        @param neighbor: The length of the neighbor list.
        @return: None
        """
        self.neighbor = neighbor

    def set_threshold_level_rate(self, threshold_level_rate):
        """
        Set the threshold level rate.

        @param threshold_level_rate: The threshold level rate.
        @return: None
        """
        self.threshold_level_rate = threshold_level_rate


if __name__ == "__main__":
    pass
