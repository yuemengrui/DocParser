# *_*coding:utf-8 *_*
# @Author : YueMengRui
import time
import torch
from ultralytics import YOLO
from doclayout_yolo import YOLOv10


def calc_area(box):
    return abs(box[2] - box[0]) * abs(box[3] - box[1])


def nms(boxes, thresh=0.3):
    true_boxes = []
    while len(boxes) > 0:
        true_boxes.append(boxes[0])
        boxes.pop(0)
        if len(boxes) == 0:
            break

        for box in boxes[::-1]:
            area = calc_area(box['box'])
            iou_x1 = max(true_boxes[-1]['box'][0], box['box'][0])
            iou_y1 = max(true_boxes[-1]['box'][1], box['box'][1])

            iou_x2 = min(true_boxes[-1]['box'][2], box['box'][2])
            iou_y2 = min(true_boxes[-1]['box'][3], box['box'][3])
            if iou_x2 - iou_x1 <= 0 or iou_y2 - iou_y1 <= 0:
                continue

            iou_area = (iou_x2 - iou_x1) * (iou_y2 - iou_y1)
            box_area = abs(true_boxes[-1]['box'][2] - true_boxes[-1]['box'][0]) * abs(
                true_boxes[-1]['box'][3] - true_boxes[-1]['box'][1])
            if iou_area / box_area > thresh or iou_area / area > thresh:
                boxes.remove(box)

    return true_boxes


class LayoutYOLO:
    def __init__(self, model_path: str, img_size: int, labels: list, model_type='yolo', device='cuda', **kwargs):
        if 'doclayout' in model_type:
            self.model = YOLOv10(model_path)
        else:
            self.model = YOLO(model_path)

        self.img_size = img_size
        self.labels = labels
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def predict(self, images, conf: float = 0.25, iou: float = 0.45, nms_threshold: float = 0.45, **kwargs):
        """
        :return: [[{'box': [x1,y1,x2,y2], 'label': '', 'score': 0.8}], []]
        """
        start = time.time()
        resp = []
        preds = self.model.predict(images, imgsz=self.img_size, conf=conf, iou=iou, device=self.device)
        for r in preds:
            temp = []
            boxes = r.boxes.cpu().numpy()
            for i in range(len(boxes.cls)):
                temp.append({
                    'box': list(map(int, boxes.xyxy[i].tolist())),
                    'label': self.labels[int(boxes.cls[i])],
                    'score': boxes.conf[i]
                })

            if nms_threshold > 0:
                temp.sort(key=lambda x: calc_area(x['box']), reverse=True)
                temp = nms(temp, thresh=nms_threshold)

            temp.sort(key=lambda x: (x['box'][1], x['box'][0]))
            resp.append(temp)

        return resp, time.time() - start
