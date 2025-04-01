## Datasetsconverter

**datasetsconverter** is a Python package for converting object detection datasets between COCO, YOLO, and PASCAL VOC formats, making it easier to work with different annotation types in computer vision projects.

### Installation

Install DatasetConverter using pip:

```bash
pip install datasetsconverter
```

### Usage

#### Convert COCO to YOLO
Convert COCO-formatted annotations to YOLO format.

```python
from datasetsconverter import coco_to_yolo

coco_to_yolo(
    coco_path="path/to/coco/annotations.json",
    output_dir="path/to/output/yolo",
    image_dir="path/to/coco/images"
)
```

#### Convert YOLO to COCO
Convert YOLO annotations into COCO format.

```python
from datasetsconverter import yolo_to_coco

yolo_to_coco(
    yolo_dir="path/to/yolo/labels",
    output_file="path/to/output/coco/annotations.json",
    image_dir="path/to/yolo/images"
)
```

#### Convert YOLO to PASCAL VOC
Transform YOLO annotations into PASCAL VOC format.

```python
from datasetsconverter import yolo_to_pascalvoc

yolo_to_pascalvoc(
    yolo_dir="path/to/yolo/labels",
    output_dir="path/to/output/pascalvoc",
    image_dir="path/to/yolo/images"
)
```

#### Convert PASCAL VOC to YOLO
Convert PASCAL VOC annotations into YOLO format.

```python
from datasetsconverter import pascalvoc_to_yolo

pascalvoc_to_yolo(
    pascalvoc_dir="path/to/pascalvoc/annotations",
    output_dir="path/to/output/yolo",
    image_dir="path/to/pascalvoc/images"
)
```

#### Convert COCO to PASCAL VOC
Convert COCO annotations into PASCAL VOC format.

```python
from datasetsconverter import coco_to_pascalvoc

coco_to_pascalvoc(
    coco_path="path/to/coco/annotations.json",
    output_dir="path/to/output/pascalvoc",
    image_dir="path/to/coco/images"
)
```

#### Convert PASCAL VOC to COCO
Convert PASCAL VOC annotations into COCO format.

```python
from datasetsconverter import pascalvoc_to_coco

pascalvoc_to_coco(
    pascalvoc_dir="path/to/pascalvoc/annotations",
    output_file="path/to/output/coco/annotations.json",
    image_dir="path/to/pascalvoc/images"
)
```
