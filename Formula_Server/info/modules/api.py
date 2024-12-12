# *_*coding:utf-8 *_*
# @Author : YueMengRui
import time
from mylogger import logger
from configs import API_LIMIT
from info import limiter, det_model, rec_model
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from info.utils.common import request_to_image, cv2pil
from info.utils.response_code import RET, error_map
from .protocol import ErrorResponse, DetRequest, DetResponse, DetOne, RecRequest, RecResponse

router = APIRouter()


@router.api_route(path='/detect', methods=['POST'], response_model=DetResponse, summary="公式检测")
@limiter.limit(API_LIMIT['base'])
def formula_det(request: Request,
                req: DetRequest
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
        resp, time_cost = det_model.predict(images, **params)
        return JSONResponse(DetResponse(data=[[DetOne(**y) for y in x] for x in resp],
                                        time_cost={'getimage': t1 - start, 'model': time_cost,
                                                   'all': time.time() - start}).dict())
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return JSONResponse(ErrorResponse(errcode=RET.SERVERERR, errmsg=error_map[RET.SERVERERR]).dict(),
                            status_code=500)


@router.api_route(path='/recognition', methods=['POST'], response_model=RecResponse, summary="公式识别")
@limiter.limit(API_LIMIT['base'])
def formula_rec(request: Request,
                req: RecRequest
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
        resp, time_cost = rec_model.predict([cv2pil(im) for im in images], **params)
        return JSONResponse(RecResponse(data=resp, time_cost={'getimage': t1 - start, 'model': time_cost,
                                                              'all': time.time() - start}).dict())
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return JSONResponse(ErrorResponse(errcode=RET.SERVERERR, errmsg=error_map[RET.SERVERERR]).dict(),
                            status_code=500)
