# *_*coding:utf-8 *_*
# @Author : YueMengRui
import time
import torch
from mylogger import logger
from info.libs.models.internvl import InternVL


class StructTable():
    def __init__(self, model_path='', device='cuda', dtype=torch.bfloat16, **kwargs):
        if not torch.cuda.is_available():
            logger.warning(f'GPU not found, model load in CPU!! slow w~ww~www～～～')
            device = 'cpu'
            dtype = torch.float32

        self.model = InternVL(
            model_path=model_path,
            dtype=dtype,
            **kwargs
        ).to(device)

    def predict(self, images, output_format: str = 'latex', max_new_tokens: int = 1024, **kwargs):
        start = time.time()
        results = self.model(images=images, output_format=output_format, max_new_tokens=max_new_tokens, **kwargs)
        return results, time.time() - start
