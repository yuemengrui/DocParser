# *_*coding:utf-8 *_*
# @Author : YueMengRui
from .myunimernet import FormulaRecognitionUniMERNet


def build_rec_model(**kwargs):
    return FormulaRecognitionUniMERNet(**kwargs)
