# *_*coding:utf-8 *_*
# @Author : YueMengRui
import time
from mylogger import logger
from configs import API_LIMIT
from info import limiter, model
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from info.utils.common import request_to_image, cv2pil
from info.utils.response_code import RET, error_map
from .protocol import ErrorResponse, TableRequest, TableResponse

router = APIRouter()


@router.api_route(path='/parser', methods=['POST'], response_model=TableResponse, summary="表格解析")
@limiter.limit(API_LIMIT['base'])
def table_parser(request: Request,
                 req: TableRequest
                 ):
    start = time.time()

    params = req.dict()

    image = params.pop('image', None)
    url = params.pop('url', None)

    images = request_to_image(image, url)
    t1 = time.time()

    if len(images) == 0:
        return JSONResponse(ErrorResponse(errcode=RET.PARAMERR, errmsg=error_map[RET.PARAMERR]).dict(), status_code=500)

    logger.info({'params': params})
    try:
        resp, time_cost = model.predict([cv2pil(im) for im in images], **params)
        return JSONResponse(TableResponse(data=resp, time_cost={'getimage': t1 - start, 'model': time_cost,
                                                                'all': time.time() - start}).dict())
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return JSONResponse(ErrorResponse(errcode=RET.SERVERERR, errmsg=error_map[RET.SERVERERR]).dict(),
                            status_code=500)
