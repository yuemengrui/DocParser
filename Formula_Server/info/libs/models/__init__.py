# *_*coding:utf-8 *_*
# @Author : YueMengRui
from info.libs.models.det import build_det_model
from info.libs.models.rec import build_rec_model


def build_model(m_type, **kwargs):
    assert m_type in ['det', 'rec']

    if m_type == 'det':
        return build_det_model(**kwargs)

    if m_type == 'rec':
        return build_rec_model(**kwargs)
