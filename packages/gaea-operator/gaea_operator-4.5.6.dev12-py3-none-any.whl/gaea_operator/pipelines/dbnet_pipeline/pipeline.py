#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/10
# @Author  : yanxiaodong
# @File    : ppyoloe_plus_m_pipeline.py
"""
from typing import List, Dict
import os
from paddleflow.pipeline import Pipeline
from paddleflow.pipeline import CacheOptions
from paddleflow.pipeline import ContainerStep
from paddleflow.pipeline import Artifact
from paddleflow.pipeline import ExtraFS
from paddleflow.pipeline import FailureOptions

from windmillmodelv1.client.model_api_model import Category

from gaea_operator.artifacts import Variable
from gaea_operator.utils import DEFAULT_TRAIN_CONFIG_FILE_NAME, \
    DEFAULT_PADDLEPADDLE_MODEL_FILE_NAME, \
    ModelTemplate, \
    Accelerator, DEFAULT_EXTEND_CONFIG_FILE_NAME
from gaea_operator.nodes import Image, Properties, set_node_parameters
from gaea_operator.nodes import Train as BaseTrain
from gaea_operator.nodes import Eval as BaseEval
from gaea_operator.nodes import Transform as BaseTransform
from gaea_operator.nodes import TransformEval, Package, Inference

NAME_TO_IMAGES = {
    BaseTrain.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name="iregistry.baidu-int.com/windmill-public/train/paddlepaddle:20250311_1741666069633"),
            Image(kind=Accelerator.KUNLUN,
                  name="iregistry.baidu-int.com/windmill-public/train/paddlepaddle:20241226_1735184045415"),
            Image(kind=Accelerator.ASCEND,
                  name=""),
        ],
    BaseEval.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name="iregistry.baidu-int.com/windmill-public/train/paddlepaddle:20250311_1741666069633"),
            Image(kind=Accelerator.KUNLUN,
                  name="iregistry.baidu-int.com/windmill-public/train/paddlepaddle:20241226_1735184045415"),
            Image(kind=Accelerator.ASCEND,
                  name=""),
        ],
    BaseTransform.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name="iregistry.baidu-int.com/windmill-public/transform:20241230_1735544464971"),
            Image(kind=Accelerator.KUNLUN,
                  name="iregistry.baidu-int.com/windmill-public/transform:20241230_1735544464971"),
            Image(kind=Accelerator.ASCEND,
                  name=""),
        ],
    TransformEval.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name="iregistry.baidu-int.com/windmill-public/inference/nvidia:1.3.7-hotfix-20241119"),
            Image(kind=Accelerator.KUNLUN,
                  name="iregistry.baidu-int.com/windmill-public/inference/kunlun:1.3.7-hotfix-20241119"),
            Image(kind=Accelerator.ASCEND,
                  name="")
        ],
    Package.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name="iregistry.baidu-int.com/windmill-public/inference/nvidia:20241230_1735546408944"),
            Image(kind=Accelerator.KUNLUN,
                  name="iregistry.baidu-int.com/windmill-public/inference/nvidia:20241230_1735546408944"),
            Image(kind=Accelerator.ASCEND,
                  name="")
        ],
    Inference.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name="iregistry.baidu-int.com/windmill-public/inference/nvidia:1.3.7-hotfix-20241119"),
            Image(kind=Accelerator.KUNLUN,
                  name="iregistry.baidu-int.com/windmill-public/inference/kunlun:1.3.7-hotfix-20241119"),
            Image(kind=Accelerator.ASCEND,
                  name="")
        ]}


@Pipeline(
    name="dbnet",
    cache_options=CacheOptions(enable=True, max_expired_time=604800),
    parallelism=6,
    failure_options=FailureOptions(strategy="continue"),
)
def pipeline(accelerator: str = "T4",
             train_accelerator: str = "V100",
             eval_accelerator: str = "V100",
             transform_accelerator: str = None,
             transform_eval_accelerator: str = None,
             package_accelerator: str = None,
             inference_accelerator: str = None,
             train_skip: int = -1,
             eval_skip: int = -1,
             transform_skip: int = -1,
             transform_eval_skip: int = -1,
             package_skip: int = -1,
             inference_skip: int = -1,
             eval_inputs: List[Variable] = None,
             transform_inputs: List[Variable] = None,
             transform_eval_inputs: List[Variable] = None,
             package_inputs: List[Variable] = None,
             inference_inputs: List[Variable] = None,
             extra_fs_name: str = "vistudio",
             extra_fs_mount_path: str = "/home/paddleflow/storage/mnt/fs-root-vistudio",
             windmill_ak: str = "",
             windmill_sk: str = "",
             org_id: str = "",
             user_id: str = "",
             windmill_endpoint: str = "",
             experiment_kind: str = "",
             experiment_name: str = "",
             modelstore_name: str = "",
             tracking_uri: str = "",
             project_name: str = "",
             scene: str = "",
             train_dataset_name: str = "",
             val_dataset_name: str = "",
             base_train_dataset_name: str = "",
             base_val_dataset_name: str = "",
             train_model_name: str = "",
             train_model_display_name: str = "",
             eval_dataset_name: str = "",
             eval_model_name: str = "",
             transform_input_model_name: str = "",
             transform_model_name: str = "",
             transform_model_display_name: str = "",
             transform_eval_input_model_name: str = "",
             transform_advanced_parameters: str = "",
             ensemble_model_name: str = "",
             ensemble_model_display_name: str = "",
             inference_input_model_name: str = ""):
    """
    Pipeline for ppyoloe_plus_m training eval transform transform-eval package inference.
    """
    base_params = {"flavour": "c4m16gpu1",
                   "queue": "qtrain",
                   "windmill_ak": windmill_ak,
                   "windmill_sk": windmill_sk,
                   "org_id": org_id,
                   "user_id": user_id,
                   "windmill_endpoint": windmill_endpoint,
                   "experiment_name": experiment_name,
                   "experiment_kind": experiment_kind,
                   "tracking_uri": tracking_uri,
                   "project_name": project_name,
                   "model_store_name": modelstore_name,
                   "scene": scene,
                   "role": "false"}
    base_env = {"PF_JOB_FLAVOUR": "{{flavour}}",
                "PF_JOB_QUEUE_NAME": "{{queue}}",
                "WINDMILL_AK": "{{windmill_ak}}",
                "WINDMILL_SK": "{{windmill_sk}}",
                "ORG_ID": "{{org_id}}",
                "USER_ID": "{{user_id}}",
                "WINDMILL_ENDPOINT": "{{windmill_endpoint}}",
                "EXPERIMENT_KIND": "{{experiment_kind}}",
                "EXPERIMENT_NAME": "{{experiment_name}}",
                "TRACKING_URI": "{{tracking_uri}}",
                "PROJECT_NAME": "{{project_name}}",
                "SCENE": "{{scene}}",
                "PIPELINE_ROLE": "windmill"}

    pre_nodes = {}
    if accelerator is None:
        accelerator = Accelerator.T4

    if train_accelerator is None:
        train_accelerator = accelerator
    train = Train(train_skip=train_skip, algorithm=ModelTemplate.DBNET_NAME, accelerator=train_accelerator)
    train.properties = Properties(images=NAME_TO_IMAGES[train.name()])
    train_step = train(base_params=base_params,
                       base_env=base_env,
                       extra_fs_name=extra_fs_name,
                       extra_fs_mount_path=extra_fs_mount_path,
                       train_dataset_name=train_dataset_name,
                       val_dataset_name=val_dataset_name,
                       base_train_dataset_name=base_train_dataset_name,
                       base_val_dataset_name=base_val_dataset_name,
                       train_model_name=train_model_name,
                       train_model_display_name=train_model_display_name)
    pre_nodes[train_step.name] = train_step

    if eval_accelerator is None:
        eval_accelerator = accelerator
    eval = Eval(eval_skip=eval_skip,
                algorithm=ModelTemplate.DBNET_NAME,
                pre_nodes=pre_nodes,
                accelerator=eval_accelerator)
    eval.inputs = eval_inputs
    eval.properties = Properties(images=NAME_TO_IMAGES[eval.name()])
    eval_step = eval(base_params=base_params,
                     base_env=base_env,
                     eval_dataset_name=eval_dataset_name,
                     eval_model_name=eval_model_name)
    pre_nodes[eval_step.name] = eval_step

    if transform_accelerator is None:
        transform_accelerator = accelerator
    transform = Transform(transform_skip=transform_skip,
                          algorithm=ModelTemplate.DBNET_NAME,
                          category=Category.CategoryImageObjectDetection.value,
                          accelerator=transform_accelerator,
                          pre_nodes=pre_nodes)
    transform.inputs = transform_inputs
    transform.properties = Properties(images=NAME_TO_IMAGES[transform.name()])
    transform_step = transform(base_params=base_params,
                               base_env=base_env,
                               train_model_name=transform_input_model_name,
                               transform_model_name=transform_model_name,
                               transform_model_display_name=transform_model_display_name,
                               advanced_parameters=transform_advanced_parameters)
    pre_nodes[transform_step.name] = transform_step

    if transform_eval_accelerator is None:
        transform_eval_accelerator = accelerator
    transform_eval = TransformEval(transform_eval_skip=transform_eval_skip,
                                   algorithm=ModelTemplate.DBNET_NAME,
                                   accelerator=transform_eval_accelerator,
                                   pre_nodes=pre_nodes)
    transform_eval.inputs = transform_eval_inputs
    transform_eval.properties = Properties(images=NAME_TO_IMAGES[transform_eval.name()])
    transform_eval_step = transform_eval(base_params=base_params,
                                         base_env=base_env,
                                         dataset_name=eval_dataset_name,
                                         transform_model_name=transform_eval_input_model_name)
    pre_nodes[transform_eval_step.name] = transform_eval_step

    if package_accelerator is None:
        package_accelerator = accelerator
    package = Package(package_skip=package_skip,
                      algorithm=ModelTemplate.DBNET_NAME,
                      accelerator=package_accelerator,
                      pre_nodes=pre_nodes)
    package.inputs = package_inputs
    package.properties = Properties(images=NAME_TO_IMAGES[package.name()])
    package_step = package(base_params=base_params,
                           base_env=base_env,
                           transform_model_name=transform_eval_input_model_name,
                           ensemble_model_name=ensemble_model_name,
                           sub_extra_models="",
                           ensemble_model_display_name=ensemble_model_display_name)
    pre_nodes[package_step.name] = package_step

    if inference_accelerator is None:
        inference_accelerator = accelerator
    inference = Inference(inference_skip=inference_skip,
                          algorithm=ModelTemplate.DBNET_NAME,
                          accelerator=inference_accelerator,
                          pre_nodes=pre_nodes)
    inference.inputs = inference_inputs
    inference.properties = Properties(images=NAME_TO_IMAGES[inference.name()])
    inference_step = inference(base_params=base_params,
                               base_env=base_env,
                               ensemble_model_name=inference_input_model_name,
                               dataset_name=eval_dataset_name)
    pre_nodes[inference_step.name] = inference_step

    return None


class Train(BaseTrain):
    """
    Train
    """
    def __init__(self, train_skip: int = -1, algorithm=ModelTemplate.DBNET_NAME, accelerator: str = Accelerator.V100):
        super().__init__(train_skip=train_skip, algorithm=algorithm, accelerator=accelerator)
        self.properties = Properties(modelFormats={
            Accelerator.NVIDIA: {f"{self.name()}.model_name": ["PaddlePaddle"]},
            Accelerator.KUNLUN: {f"{self.name()}.model_name": ["PaddlePaddle"]},
            Accelerator.ASCEND: {f"{self.name()}.model_name": ["PaddlePaddle"]},
        })

    def __call__(self,
                 base_params: dict = None,
                 base_env: dict = None,
                 extra_fs_name: str = "vistudio",
                 extra_fs_mount_path: str = "/home/paddleflow/storage/mnt/fs-root-vistudio",
                 train_dataset_name: str = "",
                 val_dataset_name: str = "",
                 base_train_dataset_name: str = "",
                 base_val_dataset_name: str = "",
                 train_model_name: str = "",
                 train_model_display_name: str = ""):
        train_params = self.set_train_params(train_dataset_name=train_dataset_name,
                                             val_dataset_name=val_dataset_name,
                                             base_train_dataset_name=base_train_dataset_name,
                                             base_val_dataset_name=base_val_dataset_name,
                                             train_model_name=train_model_name,
                                             train_model_display_name=train_model_display_name)
        train_env = self.set_train_env(extra_fs_mount_path=extra_fs_mount_path)
        train_env.update(base_env)
        train_params.update(base_params)

        train = ContainerStep(name=Train.name(),
                              docker_env=self.suggest_image(),
                              parameters=train_params,
                              env=train_env,
                              extra_fs=[ExtraFS(name=extra_fs_name, mount_path=extra_fs_mount_path)],
                              outputs={"output_model_uri": Artifact(), "output_uri": Artifact()},
                              command=f'cd /root && '
                                      f'package_path=$(python3 -c "import site; print(site.getsitepackages()[0])") && '
                                      f'python3 -m gaea_operator.nodes.train.dbnet '
                                      f'--output-model-uri={{{{output_model_uri}}}} '
                                      f'--output-uri={{{{output_uri}}}} '
                                      f'$package_path/paddleocr/tools/train.py '
                                      f'-c {{{{output_model_uri}}}}/{DEFAULT_TRAIN_CONFIG_FILE_NAME} '
                                      f'-o Global.save_model_dir={{{{output_model_uri}}}} '
                                      f'--extend_config {{{{output_model_uri}}}}/{DEFAULT_EXTEND_CONFIG_FILE_NAME}')
        if self.train_skip > 0:
            skip_parameter = "skip"
            train.condition = f"{train.parameters[skip_parameter]} < 0"

        return train


class Eval(BaseEval):
    """
    Eval
    """
    def __init__(self,
                 eval_skip: int = -1,
                 algorithm=ModelTemplate.DBNET_NAME,
                 accelerator: str = Accelerator.V100,
                 pre_nodes: Dict[str, ContainerStep] = None):
        super().__init__(eval_skip=eval_skip, algorithm=algorithm, accelerator=accelerator, pre_nodes=pre_nodes)
        self.properties = Properties(modelFormats={
            Accelerator.NVIDIA: {f"{self.name()}.model_name": ["PaddlePaddle"]},
            Accelerator.KUNLUN: {f"{self.name()}.model_name": ["PaddlePaddle"]},
            Accelerator.ASCEND: {f"{self.name()}.model_name": ["PaddlePaddle"]},
        })

    def __call__(self,
                 base_params: dict = None,
                 base_env: dict = None,
                 eval_dataset_name: str = "",
                 eval_model_name: str = ""):
        eval_params = {"skip": self.eval_skip,
                       "accelerator": self.properties.accelerator,
                       "dataset_name": eval_dataset_name,
                       "model_name": eval_model_name}
        eval_env = {"ACCELERATOR": "{{accelerator}}",
                    "DATASET_NAME": "{{dataset_name}}",
                    "MODEL_NAME": "{{model_name}}"}
        eval_env.update(base_env)
        eval_params.update(base_params)

        eval = ContainerStep(name=Eval.name(),
                             docker_env=self.suggest_image(),
                             parameters=eval_params,
                             env=eval_env,
                             outputs={"output_uri": Artifact(),
                                      "output_dataset_uri": Artifact(),
                                      "output_model_uri": Artifact()},
                             command=f'cd /root && '
                                     f'package_path=$(python3 -c "import site; print(site.getsitepackages()[0])") && '
                                     f'python3 -m gaea_operator.nodes.eval.dbnet '
                                     f'--input-model-uri={{{{input_model_uri}}}} '
                                     f'--output-uri={{{{output_uri}}}} '
                                     f'--output-dataset-uri={{{{output_dataset_uri}}}} '
                                     f'--output-model-uri={{{{output_model_uri}}}} '
                                     f'$package_path/paddleocr/tools/eval.py '
                                     f'-c {{{{output_model_uri}}}}/{DEFAULT_TRAIN_CONFIG_FILE_NAME} '
                                     f'-o Global.checkpoints={{{{output_model_uri}}}}/'
                                     f'{os.path.splitext(DEFAULT_PADDLEPADDLE_MODEL_FILE_NAME)[0]}')
        set_node_parameters(skip=self.eval_skip, step=eval, inputs=self.inputs, pre_nodes=self.pre_nodes)

        return eval


class Transform(BaseTransform):
    """
    Transform
    """

    def __init__(self,
                 transform_skip: int = -1,
                 algorithm: str = "",
                 category: str = "",
                 accelerator: str = Accelerator.T4,
                 pre_nodes: Dict[str, ContainerStep] = None):
        super().__init__(transform_skip=transform_skip,
                         algorithm=algorithm,
                         category=category,
                         accelerator=accelerator,
                         pre_nodes=pre_nodes)
        self.properties = Properties(modelFormats={
            Accelerator.NVIDIA: {
                f"{self.name()}.train_model_name": ["PaddlePaddle"],
                f"{self.name()}.transform_model_name": ["TensorRT"]},
            Accelerator.KUNLUN: {
                f"{self.name()}.train_model_name": ["PaddlePaddle"],
                f"{self.name()}.transform_model_name": ["PaddleLite"]},
            Accelerator.ASCEND: {
                f"{self.name()}.train_model_name": ["PaddlePaddle"],
                f"{self.name()}.transform_model_name": ["Other"]},
        })


if __name__ == "__main__":
    ppl = pipeline(
        accelerator="T4",
        train_accelerator="V100",
        eval_accelerator="V100",
        windmill_ak="a1a9069e2b154b2aa1a83ed12316d163",
        windmill_sk="eefac23d2660404e93855197ce60efb3",
        windmill_endpoint="http://10.27.240.5:8340",
        experiment_kind="Aim",
        experiment_name="ppyoloe_plus_m",
        tracking_uri="aim://10.27.240.5:8329",
        project_name="workspaces/internal/projects/proj-o97H2oAE",
        train_dataset_name="workspaces/internal/projects/yxdTestPipeline/datasets/ds-xplNB7iS/versions/1",
        val_dataset_name="workspaces/internal/projects/yxdTestPipeline/datasets/ds-xplNB7iS/versions/1",
        eval_dataset_name="workspaces/internal/projects/yxdTestPipeline/datasets/ds-xplNB7iS/versions/1",
        train_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/ppyoloe-plus",
        train_model_display_name="ppyoloe-plus",
        eval_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/ppyoloe-plus/versions/latest",
        transform_input_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/ppyoloe-plus/versions/latest",
        transform_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/ppyoloe-plus-t4",
        transform_model_display_name="ppyoloe-plus-t4",
        transform_eval_input_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/ppyoloe-plus-t4/"
                                        "versions/latest",
        ensemble_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/ppyoloe-plus-ensemble",
        ensemble_model_display_name="ppyoloe-plus-ensemble",
        inference_input_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/ppyoloe-plus-ensemble/"
                                   "versions/latest")

    ppl.compile(save_path="dbnet_pipeline.yaml")
    _, run_id = ppl.run(fs_name="vistudio")
