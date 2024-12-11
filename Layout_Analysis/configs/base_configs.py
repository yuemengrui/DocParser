# *_*coding:utf-8 *_*
# @Author : YueMengRui
import os

FASTAPI_TITLE = 'Layout_Analysis'
FASTAPI_HOST = '0.0.0.0'
FASTAPI_PORT = 24680

LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)
TEMP = 'temp'
os.makedirs(TEMP, exist_ok=True)

MODEL_CONFIG = '/workspace/model_config.json'

# API LIMIT
API_LIMIT = {
    "base": "10000/minute"
}
