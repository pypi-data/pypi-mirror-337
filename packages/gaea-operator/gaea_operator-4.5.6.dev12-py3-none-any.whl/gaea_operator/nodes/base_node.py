#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/6/20
# @Author  : yanxiaodong
# @File    : base_node.py
"""
from typing import List, Dict
from abc import ABCMeta, abstractmethod
import math
from paddleflow.pipeline import ContainerStep

import bcelogger

from .types import Properties
from gaea_operator.artifacts import Variable
from gaea_operator.utils import get_accelerator

EXTRA_TIME_CONSTANT = 60


class BaseNode(metaclass=ABCMeta):
    """
    BaseNode
    """
    NAME = ""
    DISPLAY_NAME = ""

    def __init__(self,
                 inputs: List[Variable] = None,
                 outputs: List[Variable] = None,
                 properties: Properties = None,
                 **kwargs):
        self._inputs = inputs
        self._outputs = outputs
        self._properties = properties

    @classmethod
    def name(cls):
        """
        name
        """
        return cls.NAME

    @classmethod
    def display_name(cls):
        """
        display_name
        """
        return cls.DISPLAY_NAME

    @property
    def inputs(self) -> List[Variable]:
        """
        input
        """
        return self._inputs

    @inputs.setter
    def inputs(self, values: List[Variable]):
        if values is not None:
            self._inputs = values

    @property
    def outputs(self) -> List[Variable]:
        """
        output
        """
        return self._outputs

    @outputs.setter
    def outputs(self, values: List[Variable]):
        if values is not None:
            self._outputs = values

    @property
    def properties(self) -> Properties:
        """
        properties
        """
        return self._properties

    @properties.setter
    def properties(self, values: Properties):
        if self._properties is None:
            self._properties = values
        else:
            for key, value in values.dict(exclude_none=True).items():
                if key == "accelerator" and value is not None and value != "":
                    accelerator_kind = get_accelerator(name=value).get_kind
                    self._properties.computeTips[accelerator_kind] = \
                        self.set_compute_tips(accelerator_kind=accelerator_kind, accelerator_name=value)
                    self._properties.flavourTips[accelerator_kind] = \
                        self.set_flavour_tips(accelerator_kind=accelerator_kind, accelerator_name=value)
                    break

            properties_dict = self._properties.dict(exclude_none=True)
            for key, value in values.dict(exclude_none=True).items():
                default_value = Properties.__fields__[key].default
                if value != default_value:
                    properties_dict[key] = value
            self._properties = Properties(**properties_dict)

    def suggest_image(self):
        """
        suggest image
        """
        for image in self.properties.images:
            # 兼容历史产线
            if hasattr(image, 'kind'):
                if image.kind == get_accelerator(self.properties.accelerator).get_kind:
                    return image.name
                continue
            accelerator = get_accelerator(self.properties.accelerator)
            if (image.acceleratorKind is not None and
                image.acceleratorKind == accelerator.get_kind) or \
                    (image.acceleratorName is not None and image.acceleratorName == accelerator.get_name):
                return image.name
        return ""

    def set_compute_tips(self, accelerator_kind: str, accelerator_name: str = None):
        """
        set compute tips
        """
        return []

    def set_flavour_tips(self, accelerator_kind: str, accelerator_name: str = None):
        """
        set compute tips
        """
        return ""

    def suggest_compute_tips(self):
        """
        suggest compute tips
        """
        if self.properties.is_pdc():
            return ""
        return self.properties.computeTips[get_accelerator(self.properties.accelerator).get_kind]

    def suggest_flavour_tips(self):
        """
        suggest favour tips
        """
        if self.properties.is_pdc:
            return "c4m16"
        return self.properties.flavourTips[get_accelerator(self.properties.accelerator).get_kind]

    def suggest_model_formats(self, key: str):
        """
        suggest model formats
        """
        # 兼容历史产线
        if isinstance(self.properties.modelFormats, dict):
            return self.properties.modelFormats[get_accelerator(self.properties.accelerator).get_kind][key]

        for format_ in self.properties.modelFormats:
            if format_.key == key and \
                    (format_.acceleratorKind is not None and
                     (format_.acceleratorKind == get_accelerator(self.properties.accelerator).get_kind) or
                     (format_.acceleratorName is not None and
                      format_.acceleratorName == get_accelerator(self.properties.accelerator).get_name)):
                return format_.formats
        return []

    def suggest_time_profiler(self):
        """
        suggest time profiler
        """
        return 0

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


def set_node_parameters(skip: int, step: ContainerStep, inputs: List[Variable], pre_nodes: Dict[str, ContainerStep]):
    """
    set node parameters
    """
    if skip > 0:
        skip_parameter = "skip"
        step.condition = f"{step.parameters[skip_parameter]} < 0"

    for variable in inputs:
        if variable.value != "" and skip < 0:
            name, value = variable.value.split(".")
            step.inputs[variable.name] = getattr(pre_nodes[name], "outputs")[value]
        else:
            step.parameters[variable.name] = ""


def calculate_train_time(benchmark: Dict,
                         epoch: int = None,
                         image_count: int = None,
                         batch_size: int = None,
                         width: int = None,
                         height: int = None,
                         eval_size: str = None,
                         gpu_num: int = None,
                         worker_num: int = None):
    """
    calculate train time profiler
    """
    if image_count is None or image_count == 0:
        bcelogger.warning("Image count is not specified, please check your dataset name")
        return 0

    if epoch is None:
        bcelogger.warning("Epoch is not specified, please check your epoch")
        return 0

    if eval_size is not None and "*" in eval_size:
        width, height = eval_size.split('*')
        width = int(width)
        height = int(height)

    # batch size coefficient
    benchmark_batch_size = benchmark["benchmark_params"].get("batch_size")
    batch_size_coefficient = benchmark["coefficients"]["batch_size"] \
        if benchmark_batch_size is not None and batch_size is not None and batch_size != benchmark_batch_size else 1
    if benchmark_batch_size is not None and batch_size is not None:
        batch_size_coefficient = benchmark_batch_size / batch_size * batch_size_coefficient \
            if batch_size > benchmark_batch_size else benchmark_batch_size / batch_size * (1 / batch_size_coefficient)
    bcelogger.info(f'Benchmark batch size is {benchmark_batch_size} '
                   f'current batch size {batch_size} and batch size coefficient: {batch_size_coefficient}')

    # width coefficient
    benchmark_width = benchmark["benchmark_params"].get("width")
    width_coefficient = benchmark["coefficients"]["width"] \
        if benchmark_width is not None and width is not None and width != benchmark_width else 1
    if benchmark_width is not None and width is not None:
        width_coefficient = width / benchmark_width * width_coefficient \
            if width > benchmark_width else width / benchmark_width * (1 / width_coefficient)
    bcelogger.info(f'Benchmark width is {benchmark_width} '
                   f'current width {width} and width coefficient: {width_coefficient}')

    # height coefficient
    benchmark_height = benchmark["benchmark_params"].get("height")
    height_coefficient = benchmark["coefficients"]["height"] \
        if benchmark_height is not None and height is not None and height != benchmark_height else 1
    if benchmark_height is not None and height is not None:
        height_coefficient = height / benchmark_height * height_coefficient \
            if height > benchmark_height else height / benchmark_height * (1 / height_coefficient)
    bcelogger.info(f'Benchmark height is {benchmark_height} '
                   f'current height {height} and height coefficient: {height_coefficient}')

    # gpu num coefficient
    benchmark_gpu_num = benchmark["benchmark_params"].get("gpu_num")
    gpu_num_coefficient = benchmark["coefficients"]["gpu_num"] \
        if benchmark_gpu_num is not None and gpu_num is not None and gpu_num != benchmark_gpu_num else 1
    if benchmark_gpu_num is not None and gpu_num is not None:
        gpu_num_coefficient = benchmark_gpu_num / gpu_num * gpu_num_coefficient
    bcelogger.info(f'Benchmark gpu num is {benchmark_gpu_num} '
                   f'current gpu num {gpu_num} and gpu num coefficient: {gpu_num_coefficient}')

    # worker num coefficient
    benchmark_worker_num = benchmark["benchmark_params"].get("worker_num")
    worker_num_coefficient = benchmark["coefficients"]["worker_num"] \
        if benchmark_worker_num is not None and worker_num is not None and worker_num != benchmark_worker_num else 1
    if benchmark_worker_num is not None and worker_num is not None:
        worker_num_coefficient = benchmark_worker_num / worker_num * worker_num_coefficient \
            if worker_num > benchmark_worker_num else benchmark_worker_num / worker_num * (1 / worker_num_coefficient)
    bcelogger.info(f'Benchmark worker num is {benchmark_worker_num} '
                   f'current worker num {worker_num} and worker num coefficient: {worker_num_coefficient}')

    coefficient = \
        batch_size_coefficient * width_coefficient * height_coefficient * gpu_num_coefficient * worker_num_coefficient

    iters_per_epoch = 1
    if image_count is not None and benchmark_batch_size is not None:
        iters_per_epoch = math.ceil(image_count / benchmark_batch_size)

    time_count = epoch * benchmark["benchmark_time"] * iters_per_epoch * coefficient + EXTRA_TIME_CONSTANT

    return time_count


def calculate_template_ensemble_time(benchmark: Dict,
                                     image_count: int = None,
                                     precision: str = None,
                                     width: int = None,
                                     height: int = None,
                                     eval_size: str = None):
    """
    calculate train time profiler
    """
    if image_count is None or image_count == 0:
        bcelogger.warning("Image count is not specified, please check your dataset name")
        return 0

    if eval_size is not None and "*" in eval_size:
        width, height = eval_size.split('*')
        width = int(width)
        height = int(height)

    # width coefficient
    benchmark_width = benchmark["benchmark_params"].get("width")
    width_coefficient = benchmark["coefficients"]["width"] \
        if benchmark_width is not None and width is not None and width != benchmark_width else 1
    if benchmark_width is not None and width is not None:
        width_coefficient = width / benchmark_width * width_coefficient \
            if width > benchmark_width else width / benchmark_width * (1 / width_coefficient)
    bcelogger.info(f'Benchmark width is {benchmark_width} '
                   f'current width {width} and width coefficient: {width_coefficient}')

    # height coefficient
    benchmark_height = benchmark["benchmark_params"].get("height")
    height_coefficient = benchmark["coefficients"]["height"] \
        if benchmark_height is not None and height is not None and height != benchmark_height else 1
    if benchmark_height is not None and height is not None:
        height_coefficient = height / benchmark_height * height_coefficient \
            if height > benchmark_height else height / benchmark_height * (1 / height_coefficient)
    bcelogger.info(f'Benchmark height is {benchmark_height} '
                   f'current height {height} and height coefficient: {height_coefficient}')

    # precision coefficient
    benchmark_precision = benchmark["benchmark_params"].get("precision")
    precision_coefficient = benchmark["coefficients"]["precision"] \
        if benchmark_precision is not None and precision is not None and precision != benchmark_precision else 1
    bcelogger.info(f'Benchmark precision is {benchmark_precision} '
                   f'current precision {precision} and precision coefficient: {precision_coefficient}')

    coefficient = width_coefficient * height_coefficient * precision_coefficient

    time_count = benchmark["benchmark_time"] * image_count * coefficient + EXTRA_TIME_CONSTANT

    return time_count
