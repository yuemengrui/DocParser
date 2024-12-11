# *_*coding:utf-8 *_*
# @Author : YueMengRui
from .struct_table_internvl import StructTable


def build_model(**kwargs):
    model = StructTable(**kwargs)
    return model
