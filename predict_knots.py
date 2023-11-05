# check pytorch installation:
# Some basic setup:
# Setup detectron2 setup_logger
import numpy as np
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import os, cv2

# import some common detectron2 utilities
from detectron2.engine import DefaultPredictor, DefaultTrainer
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

from detectron2.utils.visualizer import ColorMode
from detectron2.data.datasets import register_coco_instances
from detectron2 import model_zoo
import firebase_storage_service as storage

register_coco_instances("train_demo", {},"G:\DA\runs\labelme2coco\train_dataset_619.json", "G:\DA\images")
register_coco_instances('test_demo', {}, "G:\DA\runs\labelme2coco\test_dataset_133.json", "G:\DA\images")

test_metadata = MetadataCatalog.get('test_demo')
# test_dataset_dicts = DatasetCatalog.get('test_demo1')
def predict_image_local(img_dir):
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.WEIGHTS = os.path.join("model_final.pth")  # path to the model we just trained
    cfg.DATASETS.TRAIN = ("train_demo",)
    cfg.DATASETS.TEST = ("test_demo",)
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.6   # set a custom testing threshold
    cfg.MODEL.DEVICE = "cpu"

    predictor = DefaultPredictor(cfg)

    im = cv2.imread(img_dir)
    outputs = predictor(im)
    v = Visualizer(im[:, :, ::-1],
                    metadata= test_metadata,
                    scale=1,
                    instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels. This option is only available for segmentation models
        )
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    cv2.imwrite("images/result.jpg", out.get_image()[:, :, ::-1])
    return outputs

def predict_image_remote(imageName):
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.WEIGHTS = os.path.join("model_final.pth")  # path to the model we just trained
    cfg.DATASETS.TRAIN = ("train_demo",)
    cfg.DATASETS.TEST = ("test_demo",)
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.6   # set a custom testing threshold
    cfg.MODEL.DEVICE = "cpu"

    predictor = DefaultPredictor(cfg)
    image_path = storage.download_image(imageName)
    date = imageName.split(".")[0].split("_")[-1]
    im = cv2.imread(image_path)
    outputs = predictor(im)
    v = Visualizer(im[:, :, ::-1],
                    metadata= test_metadata,
                    scale=1,
                    instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels. This option is only available for segmentation models
        )
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    cv2.imwrite("images/result_" + date + ".jpg", out.get_image()[:, :, ::-1])
    return outputs

def get_quantity_knots(outputs):
    pred_classes = outputs["instances"].pred_classes.cpu().data.numpy
    single_knots = list(pred_classes).count(1)
    double_knots = list(pred_classes).count(0)
    return [single_knots, double_knots]

def get_average_area(outputs):
    pred_classes = outputs['instances'].pred_classes
    pred_classes = pred_classes.cpu().data.numpy()
    i = 0
    average_single = []
    average_double = []
    for pred_mask in outputs['instances'].pred_masks:
        mask = pred_mask.cpu().data.numpy().astype('uint8')
        contour, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        area = cv2.contourArea(contour[0])
        if pred_classes[i] == 0:
            average_double.append(area)
        else:
            average_single.append(area)
        i+=1
    average_area_single = sum(average_single)/len(average_single)
    average_area_double = sum(average_double)/len(average_double)
    return len(average_single), len(average_double), average_area_single, average_area_double