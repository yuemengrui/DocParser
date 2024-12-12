# *_*coding:utf-8 *_*
# @Author : YueMengRui
from pydantic import BaseModel, Field, AnyUrl, ConfigDict
from typing import List, Union, Optional, Dict, Any


class ErrorResponse(BaseModel):
    object: str = "error"
    errcode: int
    errmsg: str


class DetRequest(BaseModel):
    model_config = ConfigDict(extra='allow')

    image: Optional[Union[str, List[str]]] = Field(default=None,
                                                   description="图片base64编码，不包含base64头, 与url二选一，优先级image > url")
    url: Optional[Union[AnyUrl, List[AnyUrl]]] = Field(default=None, description="图片URL")
    conf: Optional[float] = Field(default=0.25, ge=0, le=1, description="置信度")
    iou: Optional[float] = Field(default=0.45, ge=0, le=1, description="iou")
    nms_threshold: Optional[float] = Field(default=0.45, ge=0, le=1, description="nms (if == 0 not use nms)")


class DetOne(BaseModel):
    box: List[int]
    label: str
    score: float


class DetResponse(BaseModel):
    object: str = "Formula Detect"
    data: List[List[DetOne]]
    time_cost: Dict = {}


class RecRequest(BaseModel):
    model_config = ConfigDict(extra='allow')

    image: Optional[Union[str, List[str]]] = Field(default=None,
                                                   description="图片base64编码，不包含base64头, 与url二选一，优先级image > url")
    url: Optional[Union[AnyUrl, List[AnyUrl]]] = Field(default=None, description="图片URL")


class RecResponse(BaseModel):
    object: str = "Formula Recognition"
    data: Any
    time_cost: Dict = {}
