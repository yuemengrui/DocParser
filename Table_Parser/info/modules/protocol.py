# *_*coding:utf-8 *_*
# @Author : YueMengRui
from pydantic import BaseModel, Field, AnyUrl, ConfigDict
from typing import List, Union, Optional, Dict, Literal


class ErrorResponse(BaseModel):
    object: str = "error"
    errcode: int
    errmsg: str


class TableRequest(BaseModel):
    model_config = ConfigDict(extra='allow')

    image: Optional[Union[str, List[str]]] = Field(default=None,
                                                   description="图片base64编码，不包含base64头, 与url二选一，优先级image > url")
    url: Optional[Union[AnyUrl, List[AnyUrl]]] = Field(default=None, description="图片URL")
    max_new_tokens: Optional[int] = Field(default=1024, ge=256, le=1024 * 16, description="")
    output_format: Literal['latex', 'html', 'markdown'] = Field(default="latex", description="")


class TableResponse(BaseModel):
    object: str = "Table"
    data: List[str]
    time_cost: Dict = {}
