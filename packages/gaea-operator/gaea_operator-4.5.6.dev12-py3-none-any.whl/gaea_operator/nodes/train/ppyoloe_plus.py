#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/23
# @Author  : yanxiaodong
# @File    : train_component.py
"""
import os
import json

import base64

from gaea_tracker import ExperimentTracker
from bcelogger.base_logger import setup_logger
from windmillmodelv1.client.model_api_model import parse_model_name
from windmillmodelv1.client.model_api_model import ModelName
from windmillmodelv1.client.model_api_modelstore import parse_modelstore_name
from windmillclient.client.windmill_client import WindmillClient
import bcelogger

from gaea_operator.dataset import CocoDataset
from gaea_operator.config import PPYOLOEPLUSMConfig, KEY_NETWORK_ARCHITECTURE, KEY_EARLY_STOPPING
from gaea_operator.metric.types.metric import LOSS_METRIC_NAME, \
    MAP_METRIC_NAME, \
    AP50_METRIC_NAME, \
    AR_METRIC_NAME, \
    BOUNDING_BOX_MEAN_AVERAGE_PRECISION_METRIC_NAME
from gaea_operator.trainer import Trainer
from gaea_operator.model import Model
from gaea_operator.metric import get_score_from_file, update_metric_file_with_dataset
from gaea_operator.utils import write_file, is_base64, ModelTemplate
from gaea_operator.argument.train_args import parse_args


def ppyoloe_plus_train(args):
    """
    Train component for ppyoloe_plus model.
    """
    windmill_client = WindmillClient(ak=args.windmill_ak,
                                     sk=args.windmill_sk,
                                     endpoint=args.windmill_endpoint,
                                     context={"OrgID": args.org_id, "UserID": args.user_id})
    tracker_client = ExperimentTracker(windmill_client=windmill_client,
                                       tracking_uri=args.tracking_uri,
                                       experiment_name=args.experiment_name,
                                       experiment_kind=args.experiment_kind,
                                       project_name=args.project_name)
    setup_logger(config=dict(file_name=os.path.join(args.output_uri, "worker.log")))
    is_pdc = True if args.is_pdc.lower() == "true" else False
    if is_pdc:
        dataset_uri = os.path.join(os.path.dirname(args.output_uri), "dataset")
    else:
        dataset_uri = "/home/windmill/tmp/dataset"
    coco_dataset = CocoDataset(windmill_client=windmill_client,
                               work_dir=tracker_client.work_dir,
                               extra_work_dir=tracker_client.extra_work_dir)
    if args.scene is not None and len(args.scene) > 0:
        bcelogger.info(f"Scene: {args.scene}")
        tags = [{"scene": args.scene}]
        response = windmill_client.list_model(workspace_id=parse_modelstore_name(args.public_model_store).workspace_id,
                                              model_store_name=parse_modelstore_name(
                                                  args.public_model_store).local_name,
                                              tags=tags)
        if len(response.result) == 0:
            bcelogger.warning(f"No model found with tags: {tags}")
        for model in response.result:
            model_name = model["name"]
            bcelogger.info(f"Model: {model_name}")
            if "baseDatasetName" in model["artifact"]["tags"]:
                args.base_train_dataset_name = model["artifact"]["tags"]["baseDatasetName"]
                args.base_val_dataset_name = model["artifact"]["tags"]["baseDatasetName"]

    # 1. 合并train分片数据集
    coco_dataset.concat_dataset(dataset_name=args.train_dataset_name,
                                base_dataset_name=args.base_train_dataset_name,
                                output_dir=dataset_uri,
                                usage=CocoDataset.usages[0])

    # 2. 合并val分片数据集
    coco_dataset.concat_dataset(dataset_name=args.val_dataset_name,
                                base_dataset_name=args.base_val_dataset_name,
                                output_dir=dataset_uri,
                                usage=CocoDataset.usages[1])

    # 兼容json串传入
    if is_base64(args.advanced_parameters):
        train_advanced_parameters = json.loads(base64.b64decode(args.advanced_parameters))
    else:
        train_advanced_parameters = json.loads(args.advanced_parameters)
    model_template = ModelTemplate(algorithm=ModelTemplate.PPYOLOE_PLUS_NAME)
    train_advanced_parameters[KEY_NETWORK_ARCHITECTURE] = \
        model_template.suggest_network_architecture(train_advanced_parameters[KEY_NETWORK_ARCHITECTURE])
    bcelogger.info(f"Advanced parameters: {train_advanced_parameters}")
    # 3. 下载预训练模型
    pretrain = {"ppyoloe_s": "ppyoloe_crn_s_obj365_pretrained",
                "ppyoloe_m": "ppyoloe_crn_m_obj365_pretrained",
                "ppyoloe_l": "ppyoloe_crn_l_obj365_pretrained",
                "ppyoloe_x": "ppyoloe_crn_x_obj365_pretrained"}
    pretrain_name = pretrain[train_advanced_parameters[KEY_NETWORK_ARCHITECTURE]]
    pretrain_name = ModelName(workspace_id=parse_modelstore_name(args.public_model_store).workspace_id,
                              model_store_name=parse_modelstore_name(args.public_model_store).local_name,
                              local_name=pretrain_name).get_name()
    bcelogger.info(f"Pretrain model name: {pretrain_name}")
    if is_pdc:
        pretrain_model_uri = os.path.join(os.path.dirname(args.output_uri), "pretrain")
    else:
        pretrain_model_uri = "/home/windmill/tmp/pretrain"
    windmill_client.download_artifact(object_name=pretrain_name, version="latest", output_uri=pretrain_model_uri)

    # 4. 生成训练配置文件，固定名字 train_config.yaml，保存在 model_uri
    config = PPYOLOEPLUSMConfig(windmill_client=windmill_client, tracker_client=tracker_client)
    config.write_train_config(dataset_uri=dataset_uri,
                              model_uri=args.output_model_uri,
                              advanced_parameters=train_advanced_parameters,
                              pretrain_model_uri=pretrain_model_uri)
    early_stopping_parameters = {}
    early_stopping_parameters["is_early_stopping"] = args.is_early_stopping
    early_stopping_parameters["early_stopping_patience"] = args.early_stopping_patience
    extend_parameters = {KEY_EARLY_STOPPING: early_stopping_parameters}
    config.write_extend_config(model_uri=args.output_model_uri, extend_parameters=extend_parameters)
    metric_names = [LOSS_METRIC_NAME, MAP_METRIC_NAME, AP50_METRIC_NAME, AR_METRIC_NAME]
    trainer = Trainer(framework="PaddlePaddle", tracker_client=tracker_client)
    trainer.track_model_score(metric_names=metric_names)
    # 5. 训练
    if is_pdc:
        os.environ["IMAGE"] = args.image
        os.environ["PDC_PARAMS"] = args.pdc_params
        os.environ["OUTPUT_URI"] = args.output_uri
        trainer.pdc_launch()
    else:
        trainer.track_train_log(output_uri=args.output_uri)
        trainer.launch()

    trainer.paddledet_export(model_dir=args.output_model_uri)

    # 6. 更新指标文件
    update_metric_file_with_dataset(dataset_name=args.train_dataset_name,
                                    input_dir=args.output_model_uri,
                                    file_name="metric.json")

    # 7. 创建模型
    metric_name = BOUNDING_BOX_MEAN_AVERAGE_PRECISION_METRIC_NAME
    current_score = get_score_from_file(filepath=os.path.join(args.output_model_uri, "metric.json"),
                                        metric_name=metric_name)
    best_score, version = Model(windmill_client=windmill_client). \
        get_best_model_score(model_name=args.model_name, metric_name=metric_name)
    tags = {metric_name: str(current_score)}
    alias = None
    if current_score >= best_score and version is not None:
        alias = ["best"]
        bcelogger.info(
            f"{metric_name.capitalize()} current score {current_score} >= {best_score}, update [best]")
        tags.update(
            {"bestReason": f"current.score({current_score}) greater than {version}.score({best_score})"})
    if version is None:
        alias = ["best"]
        bcelogger.info(f"First alias [best] score: {current_score}")
        tags.update({"bestReason": f"current.score({current_score})"})

    model_name = parse_model_name(args.model_name)
    workspace_id = model_name.workspace_id
    model_store_name = model_name.model_store_name
    local_name = model_name.local_name
    response = windmill_client.create_model(workspace_id=workspace_id,
                                            model_store_name=model_store_name,
                                            local_name=local_name,
                                            display_name=args.model_display_name,
                                            category="Image/ObjectDetection",
                                            model_formats=["PaddlePaddle"],
                                            artifact_alias=alias,
                                            artifact_tags=tags,
                                            artifact_metadata=config.metadata,
                                            artifact_uri=args.output_model_uri)
    bcelogger.info(f"Model {args.model_name} created response: {response}")

    # 7. 输出文件
    write_file(obj=json.loads(response.raw_data)["artifact"], output_dir=args.output_model_uri)


if __name__ == "__main__":
    args = parse_args()
    ppyoloe_plus_train(args=args)
