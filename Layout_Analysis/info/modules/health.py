# *_*coding:utf-8 *_*
# @Author : YueMengRui
from fastapi import APIRouter, Request
from info import limiter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.api_route(path='/ai/health', methods=['GET'], summary="health", include_in_schema=False)
@limiter.limit("120/minute")
async def health(request: Request):
    return JSONResponse({'msg': 'I am very healthy'})
