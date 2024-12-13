# *_*coding:utf-8 *_*
# @Author : YueMengRui
import os
import time
import torch
import argparse
import unimernet.tasks as tasks
from unimernet.common.config import Config
from unimernet.processors import load_processor
from mylogger import logger


class FormulaRecognitionUniMERNet:
    def __init__(self, model_path: str, **kwargs):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_dir = model_path
        self.cfg_path = None
        for fil in os.listdir(self.model_dir):
            if fil.endswith('yaml'):
                self.cfg_path = os.path.join(self.model_dir, fil)
                break

        # Load the UniMERNet model
        self.model, self.vis_processor = self.load_model_and_processor()

    def load_model_and_processor(self):
        try:
            args = argparse.Namespace(cfg_path=self.cfg_path, options=None)
            cfg = Config(args)
            cfg.config.model.pretrained = os.path.join(self.model_dir, "pytorch_model.pth")
            cfg.config.model.model_config.model_name = self.model_dir
            cfg.config.model.tokenizer_config.path = self.model_dir
            task = tasks.setup_task(cfg)
            model = task.build_model(cfg).to(self.device)
            vis_processor = load_processor('formula_image_eval',
                                           cfg.config.datasets.formula_rec_eval.vis_processor.eval)
            return model, vis_processor
        except Exception as e:
            logger.error(f"Error loading model and processor: {e}")
            raise

    def predict(self, images, **kwargs):
        start = time.time()
        results = []
        for image in images:
            # Process the image using the visual processor and prepare it for the model
            image = self.vis_processor(image).unsqueeze(0).to(self.device)

            # Generate the prediction using the model
            output = self.model.generate({"image": image})
            pred = output["pred_str"][0]

            results.append(pred)

        return results, time.time() - start
