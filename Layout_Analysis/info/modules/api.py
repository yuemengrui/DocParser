# *_*coding:utf-8 *_*
# @Author : YueMengRui
from info import limiter, model
from mylogger import logger
from configs import API_LIMIT
from .protocol import LayoutRequest
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request

router = APIRouter()


@router.api_route(path='/analysis', methods=['POST'], summary="版面分析")
@limiter.limit(API_LIMIT['base'])
def layout_analysis(request: Request,
                    req: LayoutRequest
                    ):
    logger.info(req.dict())

    return JSONResponse({'code': 200, 'msg': u'成功'})
