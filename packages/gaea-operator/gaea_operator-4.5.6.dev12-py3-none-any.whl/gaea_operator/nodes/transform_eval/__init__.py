#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/21
# @Author  : yanxiaodong
# @File    : __init__.py.py
"""
from typing import Dict, List
from paddleflow.pipeline import ContainerStep
from paddleflow.pipeline import Artifact

import bcelogger

from ..base_node import BaseNode, set_node_parameters, calculate_template_ensemble_time
from ..types import Properties, ModelFormat
from gaea_operator.artifacts import Variable
from gaea_operator.utils import get_accelerator, Accelerator, ModelTemplate


class TransformEval(BaseNode):
    """
    Transform
    """
    NAME = "transform-eval"
    DISPLAY_NAME = "模型转换评估"

    def __init__(self,
                 config: Dict = None,
                 transform_eval_skip: int = -1,
                 algorithm: str = "",
                 accelerator: str = Accelerator.T4,
                 pre_nodes: Dict[str, ContainerStep] = None):
        if config is None:
            # 兼容历史产线
            model_formats = {
                Accelerator.NVIDIA: {f"{self.name()}.model_name": ["TensorRT"]},
                Accelerator.KUNLUN: {f"{self.name()}.model_name": ["PaddleLite"]},
                Accelerator.ASCEND: {f"{self.name()}.model_name": ["Other"]},
            }
        else:
            model_formats = []
            for model in config["models"]:
                if "acceleratorKind" in model:
                    model_formats.append(ModelFormat(key=f'{self.name()}.{model["key"]}',
                                                     acceleratorKind=model["acceleratorKind"],
                                                     formats=model["modelFormats"]))
                elif "acceleratorName" in model:
                    model_formats.append(ModelFormat(key=f'{self.name()}.{model["key"]}',
                                                     acceleratorName=model["acceleratorName"],
                                                     formats=model["modelFormats"]))
                else:
                    raise ValueError(f"Config model acceleratorKind or acceleratorName must be specified, "
                                     f"but got {model}")

        properties = Properties(accelerator=accelerator,
                                computeTips={
                                    Accelerator.NVIDIA: self.set_compute_tips(accelerator_kind=Accelerator.NVIDIA),
                                    Accelerator.KUNLUN: self.set_compute_tips(accelerator_kind=Accelerator.KUNLUN),
                                    Accelerator.ASCEND: self.set_compute_tips(accelerator_kind=Accelerator.ASCEND),
                                },
                                flavourTips={
                                    Accelerator.NVIDIA: self.set_flavour_tips(accelerator_kind=Accelerator.NVIDIA),
                                    Accelerator.KUNLUN: self.set_flavour_tips(accelerator_kind=Accelerator.KUNLUN),
                                    Accelerator.ASCEND: self.set_flavour_tips(accelerator_kind=Accelerator.ASCEND),
                                },
                                modelFormats=model_formats)

        inputs: List[Variable] = \
            [
                Variable(type="model", name="input_model_uri", value="transform.output_model_uri"),
                Variable(type="dataset", name="input_dataset_uri", value="eval.output_dataset_uri")
            ]
        outputs: List[Variable] = \
            [
                Variable(type="dataset",
                         name="output_dataset_uri",
                         displayName="模型转换评估的数据",
                         key=f"{self.name()}.model_name",
                         value="transform-eval.output_dataset_uri")
            ]

        super().__init__(inputs=inputs, outputs=outputs, properties=properties)

        self.transform_eval_skip = transform_eval_skip
        self.algorithm = algorithm
        self.pre_nodes = pre_nodes

    def suggest_time_profiler(self):
        """
        suggest time profiler
        """
        model_template = ModelTemplate(accelerator=self.properties.accelerator)
        time_profiler_params = model_template.suggest_time_profiler(
            key=self.properties.timeProfilerParams.networkArchitecture, node_name=self.name())

        time_count = calculate_template_ensemble_time(benchmark=time_profiler_params,
                                                      image_count=self.properties.timeProfilerParams.evalImageCount,
                                                      width=self.properties.timeProfilerParams.width,
                                                      height=self.properties.timeProfilerParams.height,
                                                      eval_size=self.properties.timeProfilerParams.evalSize,
                                                      precision=self.properties.timeProfilerParams.precision)
        bcelogger.info(f"Transform eval time count: {time_count}")

        return time_count

    def set_compute_tips(self, accelerator_kind: str, accelerator_name: str = None):
        """
        set compute tips
        """
        accelerator = get_accelerator(kind=accelerator_kind, name=accelerator_name)
        return ["training", f"tags.accelerator={accelerator.get_name}"] + accelerator.suggest_resource_tips()

    def set_flavour_tips(self, accelerator_kind: str = None, accelerator_name: str = None):
        """
        set compute tips
        """
        accelerator = get_accelerator(kind=accelerator_kind, name=accelerator_name)
        return accelerator.suggest_flavour_tips()

    def __call__(self,
                 base_params: dict = None,
                 base_env: dict = None,
                 dataset_name: str = "",
                 transform_model_name: str = ""):
        transform_eval_params = {"skip": self.transform_eval_skip,
                                 "accelerator": self.properties.accelerator,
                                 "dataset_name": dataset_name,
                                 "model_name": transform_model_name,
                                 "advanced_parameters": '{"conf_threshold":"0.5",'
                                                        '"iou_threshold":"0.5"}'}
        transform_eval_env = {"ACCELERATOR": "{{accelerator}}",
                              "DATASET_NAME": "{{dataset_name}}",
                              "MODEL_NAME": "{{model_name}}",
                              "ADVANCED_PARAMETERS": "{{advanced_parameters}}"}
        transform_eval_params.update(base_params)
        transform_eval_env.update(base_env)
        accelerator = get_accelerator(name=self.properties.accelerator)
        transform_eval_env.update(accelerator.suggest_env())

        transform_eval = ContainerStep(name=TransformEval.name(),
                                       docker_env=self.suggest_image(),
                                       env=transform_eval_env,
                                       parameters=transform_eval_params,
                                       outputs={"output_uri": Artifact(), "output_dataset_uri": Artifact()},
                                       command=f'cd /root && '
                                               f'python3 -m gaea_operator.nodes.transform_eval.transform_eval '
                                               f'--algorithm={self.algorithm} '
                                               f'--input-model-uri={{{{input_model_uri}}}} '
                                               f'--input-dataset-uri={{{{input_dataset_uri}}}} '
                                               f'--output-dataset-uri={{{{output_dataset_uri}}}} '
                                               f'--output-uri={{{{output_uri}}}}')
        set_node_parameters(skip=self.transform_eval_skip,
                            step=transform_eval,
                            inputs=self.inputs,
                            pre_nodes=self.pre_nodes)

        return transform_eval