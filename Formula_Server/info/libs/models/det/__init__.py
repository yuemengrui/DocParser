# *_*coding:utf-8 *_*
# @Author : YueMengRui
from .yolo import DetYOLO


def build_det_model(**kwargs):
    return DetYOLO(**kwargs)
