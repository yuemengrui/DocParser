# *_*coding:utf-8 *_*
from fastapi import FastAPI
from . import api, health


def register_router(app: FastAPI):
    app.include_router(router=api.router, prefix="/ai/docparser/table", tags=['Table'])
    app.include_router(router=health.router, prefix="", tags=['health'])