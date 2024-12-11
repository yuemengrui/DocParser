# *_*coding:utf-8 *_*
# @Author : YueMengRui
from .layout_yolo import LayoutYOLO


def build_model(model_type: str, **kwargs):
    if 'yolo' in model_type:
        model = LayoutYOLO(model_type=model_type, **kwargs)
        return model
