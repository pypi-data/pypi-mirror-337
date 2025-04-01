import os
from datasetsconverter import coco_to_yolo, yolo_to_coco


def test_coco_to_yolo():
    # Example test for coco_to_yolo
    assert callable(coco_to_yolo)


def test_yolo_to_coco():
    # Example test for yolo_to_coco
    assert callable(yolo_to_coco)
