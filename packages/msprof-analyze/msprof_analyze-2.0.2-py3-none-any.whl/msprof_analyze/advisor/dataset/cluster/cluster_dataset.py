# Copyright (c) 2024, Huawei Technologies Co., Ltd.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0  (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging

import os
import re

from collections import defaultdict
from msprof_analyze.advisor.dataset.dataset import Dataset
from msprof_analyze.prof_common.singleton import singleton
from msprof_analyze.prof_common.file_manager import FileManager
from msprof_analyze.prof_common.constant import Constant
from msprof_analyze.cluster_analyse.cluster_analysis import Interface
from msprof_analyze.advisor.dataset.cluster.cluster_step_trace_time_bean import ClusterStepTraceTimeBean
from msprof_analyze.advisor.dataset.cluster.hccl_collection import HcclInfo

logger = logging.getLogger()


class ClusterDataset(Dataset):

    def __init__(self, collection_path, data: dict, **kwargs) -> None:
        super().__init__(collection_path, data, **kwargs)

    def is_cluster_analysis_output_exist(self):
        """
        check whether input path is valid
        """
        for filename in os.listdir(self.output_path):
            if filename == 'cluster_analysis_output':
                logger.info("Cluster has been analyzed "
                            "because of the existence of cluster analysis output directory.")
                logger.info("Skip Cluster analyze backend.")
                return True
        return False

    def cluster_analyze(self):
        if self.is_cluster_analysis_output_exist():
            return
        parameter = {
            Constant.PROFILING_PATH: self.collection_path,
            Constant.MODE: "all",
            Constant.CLUSTER_ANALYSIS_OUTPUT_PATH: self.output_path
        }
        logger.info("cluster analysis is in the process, please wait...")
        try:
            Interface(parameter).run()
        except Exception as e:
            raise ValueError(f"Cluster analyze backend failed:{e}") from e

    def load_csv_data(self, file_name, data_bean):
        csv_path = os.path.join(self.output_path, Constant.CLUSTER_ANALYSIS_OUTPUT, file_name)
        if not os.path.exists(csv_path):
            msg = "[ERROR] cluster_step_trace_time.csv doesn't exist, terminate analysis."
            raise RuntimeError(msg)
        data = FileManager.read_csv_file(csv_path, data_bean)
        return data

    def load_json_data(self, file_name):
        json_path = os.path.join(self.output_path, Constant.CLUSTER_ANALYSIS_OUTPUT, file_name)
        if not os.path.exists(json_path):
            msg = "[ERROR] cluster_communication.json doesn't exist, terminate analysis."
            raise RuntimeError(msg)
        data = FileManager.read_json_file(json_path)
        return data


@singleton
class ClusterStepTraceTimeDataset(ClusterDataset):
    RANK = "rank"
    STAGE = "stage"

    def __init__(self, collection_path: str, data: dict, **kwargs):
        self._step_dict = defaultdict()
        self._stages = []
        super().__init__(collection_path, data, **kwargs)

    def format_data(self, step_data: list):
        step_dict = defaultdict(lambda: [0, 0, 0])
        for step_bean in step_data:
            if step_bean.type == self.RANK:
                step_rank_record = []
                step = str(step_bean.step).replace(" ", "") or str(Constant.DEFAULT_STEP)
                rank = str(step_bean.index).replace(" ", "")
                if step:
                    step_rank_record.append(step)
                if rank:
                    step_rank_record.append(rank)

                step_rank_index = Constant.STEP_RANK_SEP.join(step_rank_record)
                step_dict[step_rank_index][0] += step_bean.compute
                step_dict[step_rank_index][1] += step_bean.communication
                step_dict[step_rank_index][2] += step_bean.free
            if step_bean.type == self.STAGE:
                stage = sorted(list(map(int, re.findall(r'\d+', step_bean.stage))))
                if stage in self._stages:
                    continue
                self._stages.append(stage)
        return step_dict

    def get_data(self):
        return self._step_dict

    def get_stages(self):
        return sorted(self._stages)

    def _parse(self):
        self.cluster_analyze()
        try:
            step_data = self.load_csv_data(Constant.CLUSTER_STEP_TIME_CSV, ClusterStepTraceTimeBean)
        except RuntimeError as e:
            logger.error("捕获到异常：%s", e)
            self._step_dict = None
            return False
        self._step_dict = self.format_data(step_data)
        return True


@singleton
class ClusterCommunicationDataset(ClusterDataset):
    RDMA_TIME_MS = "RDMA time(ms)"
    RDMA_SIZE_MB = "RDMA size(mb)"
    SDMA_TIME_MS = "SDMA time(ms)"
    SDMA_SIZE_MB = "SDMA size(mb)"
    RDMA_BANDWIDTH = "RDMA bandwidth(GB/s)"
    SDMA_BANDWIDTH = "SDMA bandwidth(GB/s)"
    COMMUNICATION_BANDWIDTH_INFO = "Communication Bandwidth Info"
    TRANSIT_TIME = "Transit Time(ms)"
    TRANSIT_SIZE = "Transit Size(MB)"
    SDMA = "SDMA"
    RDMA = "RDMA"

    def __init__(self, collection_path: str, data: dict, **kwargs):
        self.rank_bw_dict = defaultdict(self.create_rank_bw_dict)
        self.hccl_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        super().__init__(collection_path, data, **kwargs)

    @staticmethod
    def compute_ratio(dividend: float, divisor: float):
        if abs(divisor) < 1e-15:
            return 0
        else:
            return round(dividend / divisor, 4)
    
    def create_rank_bw_dict(self):
        return {
            self.RDMA_TIME_MS: 0,
            self.RDMA_SIZE_MB: 0,
            self.SDMA_TIME_MS: 0,
            self.SDMA_SIZE_MB: 0,
        }

    def process(self, communication_json: dict):
        for comm_group, group_dict in communication_json.items():
            if self.hccl_dict.get(comm_group) is None:
                self.hccl_dict.setdefault(comm_group, defaultdict(lambda: defaultdict(list)))
            for step, step_dict in group_dict.items():
                for op, op_dict in step_dict.items():
                    self.compute_bandwidth(step.lower().lstrip("step") or str(Constant.DEFAULT_STEP), op_dict)
                    self.process_hccl_info(comm_group, step, op, op_dict)

    def process_hccl_info(self, group, step, op, op_dict):
        op_name = op.split("@")[0]
        for rank_id, rank_dict in op_dict.items():
            try:
                hccl_info = HcclInfo(group, step, rank_id, op, rank_dict)
                if self.hccl_dict[group].get(op_name) is None:
                    self.hccl_dict[group].setdefault(op_name, defaultdict(list))
                if self.hccl_dict[group][op_name].get(step) is None:
                    self.hccl_dict[group][op_name].setdefault(step, list())
                self.hccl_dict[group][op_name][step].append(hccl_info)
            except ValueError as e:
                msg = "[ERROR] Cluster_communication.json has invalid structure."
                raise ValueError(msg) from e

    def compute_bandwidth(self, step, op_dict: dict):
        for rank_id, rank_dict in op_dict.items():
            try:
                rank = int(rank_id)
            except ValueError as e:
                msg = "[ERROR] Cluster_communication.json has invalid structure."
                raise ValueError(msg) from e
            for comm_type, bw_dict in rank_dict.get(self.COMMUNICATION_BANDWIDTH_INFO, {}).items():
                if comm_type == self.SDMA:
                    self.rank_bw_dict[f"{step}{Constant.STEP_RANK_SEP}{rank}"][self.SDMA_SIZE_MB] += \
                        bw_dict.get(self.TRANSIT_SIZE)
                    self.rank_bw_dict[f"{step}{Constant.STEP_RANK_SEP}{rank}"][self.SDMA_TIME_MS] += \
                        bw_dict.get(self.TRANSIT_TIME)
                if comm_type == self.RDMA:
                    self.rank_bw_dict[f"{step}{Constant.STEP_RANK_SEP}{rank}"][self.RDMA_SIZE_MB] += \
                        bw_dict.get(self.TRANSIT_SIZE)
                    self.rank_bw_dict[f"{step}{Constant.STEP_RANK_SEP}{rank}"][self.RDMA_TIME_MS] += \
                        bw_dict.get(self.TRANSIT_TIME)

        for step_rank in self.rank_bw_dict.keys():
            self.rank_bw_dict[step_rank][self.RDMA_BANDWIDTH] = self.compute_ratio(
                self.rank_bw_dict[step_rank][self.RDMA_SIZE_MB], self.rank_bw_dict[step_rank][self.RDMA_TIME_MS])
            self.rank_bw_dict[step_rank][self.SDMA_BANDWIDTH] = self.compute_ratio(
                self.rank_bw_dict[step_rank][self.SDMA_SIZE_MB], self.rank_bw_dict[step_rank][self.SDMA_TIME_MS])

    def get_data(self):
        return self.rank_bw_dict

    def _parse(self):
        self.cluster_analyze()
        try:
            communication_json = self.load_json_data(Constant.CLUSTER_COMM_JSON)
        except RuntimeError as e:
            logger.error("捕获到异常：%s", e)
            self.rank_bw_dict = None
            return False
        self.process(communication_json)
        return True
