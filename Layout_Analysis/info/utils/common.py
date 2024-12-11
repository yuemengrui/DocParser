# *_*coding:utf-8 *_*
# @Author : YueMengRui
import os
import shutil
import cv2
import base64
import requests
import numpy as np
from mylogger import logger


class DotDict(dict):
    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        value = self[key]
        if isinstance(value, dict):
            value = DotDict(value)
        return value


def boxes_n_to_4(points):
    if len(points) == 0:
        return []

    box = np.array(points).reshape((-1, 2))
    x_min = int(min(box[:, 0]))
    x_max = int(max(box[:, 0]))
    y_min = int(min(box[:, 1]))
    y_max = int(max(box[:, 1]))

    return [x_min, y_min, x_max, y_max]


def cv2_to_base64(image):
    return base64.b64encode(np.array(cv2.imencode('.jpg', image)[1]).tobytes()).decode('utf-8')


def base64_to_cv2(b64str: str):
    data = base64.b64decode(b64str.encode('utf-8'))
    data = np.frombuffer(data, np.uint8)
    data = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return data


def bytes_to_cv2(data: bytes):
    data = np.frombuffer(data, np.uint8)
    data = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return data


def cv2_to_bytes(image):
    _, img_encode = cv2.imencode('.jpg', image)
    img_bytes = img_encode.tobytes()
    return img_bytes


def request_to_image(image, url):
    images = []
    if image:
        try:
            if isinstance(image, list):
                for im in image:
                    images.append(base64_to_cv2(im))
            else:
                images.append(base64_to_cv2(image))
        except Exception as e:
            logger.error({'EXCEPTION': e})

    if len(images) > 0:
        return images

    if url:
        try:
            if isinstance(url, list):
                for u in url:
                    images.append(bytes_to_cv2(requests.get(u).content))
            else:
                images.append(bytes_to_cv2(requests.get(url).content))
        except Exception as e:
            logger.error({'EXCEPTION': e})

    return images


def resize_4096(img):
    scale = 1
    h, w = img.shape[:2]

    if max(h, w) > 4096:
        scale = 4096 / max(h, w)
        img = cv2.resize(img, dsize=None, fx=scale, fy=scale)

    return img, scale


def delete_temp(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)
        else:
            os.remove(path)
    except:
        pass
