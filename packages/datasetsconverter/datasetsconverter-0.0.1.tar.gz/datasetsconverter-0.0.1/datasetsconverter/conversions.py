import os
import json
import shutil
from pathlib import Path
from tqdm import tqdm
from PIL import Image
import xml.etree.ElementTree as ET


class DatasetConverter:
    def __init__(self):
        """
        Initialize the DatasetConverter class.
        """
        pass

    def coco_to_yolo(self, coco_path: str, output_dir: str, image_dir: str):
        """
        Convert a COCO dataset to YOLO format and rearrange images.

        Args:
            coco_path (str): Path to the COCO annotations file (e.g., _annotations.coco.json).
            output_dir (str): Directory to save the YOLO-formatted dataset.
            image_dir (str): Directory containing the images referenced in the COCO dataset.
        """
        try:
            # Ensure output directories exist
            labels_dir = os.path.join(output_dir, "labels")
            images_dir = os.path.join(output_dir, "images")
            os.makedirs(labels_dir, exist_ok=True)
            os.makedirs(images_dir, exist_ok=True)

            # Load COCO annotations
            with open(coco_path, "r") as f:
                coco_data = json.load(f)

            # Extract categories (class names)
            categories = {
                category["id"]: category["name"] for category in coco_data["categories"]
            }

            # Process each image and its annotations
            for image in tqdm(coco_data["images"], desc="Converting COCO to YOLO"):
                image_id = image["id"]
                image_filename = image["file_name"]
                image_width = image["width"]
                image_height = image["height"]

                # Copy image to YOLO images directory
                src_image_path = os.path.join(image_dir, image_filename)
                dst_image_path = os.path.join(images_dir, image_filename)
                if not os.path.exists(src_image_path):
                    print(f"Warning: Image {src_image_path} not found. Skipping.")
                    continue
                shutil.copy(src_image_path, dst_image_path)

                # Create a corresponding YOLO label file
                label_file_path = os.path.join(
                    labels_dir, f"{Path(image_filename).stem}.txt"
                )
                with open(label_file_path, "w") as label_file:
                    for annotation in coco_data["annotations"]:
                        if annotation["image_id"] == image_id:
                            category_id = annotation["category_id"]
                            bbox = annotation[
                                "bbox"
                            ]  # COCO format: [x_min, y_min, width, height]

                            # Convert COCO bbox to YOLO format: [class_id, x_center, y_center, width, height]
                            x_min, y_min, width, height = bbox
                            x_center = (x_min + width / 2) / image_width
                            y_center = (y_min + height / 2) / image_height
                            width /= image_width
                            height /= image_height

                            # Write YOLO annotation
                            label_file.write(
                                f"{category_id} {x_center} {y_center} {width} {height}\n"
                            )

            # Save class names to a file
            with open(os.path.join(output_dir, "classes.txt"), "w") as class_file:
                for category_id, category_name in categories.items():
                    class_file.write(f"{category_name}\n")

            print(
                f"COCO to YOLO conversion completed. YOLO dataset saved to {output_dir}"
            )

        except Exception as e:
            print(f"Error during COCO to YOLO conversion: {e}")

    def yolo_to_coco(self, yolo_dir: str, output_file: str, image_dir: str):
        """
        Convert a YOLO dataset to COCO format and rearrange images.

        Args:
            yolo_dir (str): Path to the YOLO labels directory.
            output_file (str): Path to save the COCO annotations file.
            image_dir (str): Path to the directory containing images.
        """
        try:
            # Ensure the output directory exists
            output_dir = os.path.dirname(output_file)

            os.makedirs(output_dir, exist_ok=True)

            # Load class names from YOLO classes.txt
            classes_file = os.path.join(yolo_dir, "classes.txt")
            with open(classes_file, "r") as f:
                class_names = [line.strip() for line in f.readlines()]

            # Initialize COCO structure
            coco_data = {
                "info": {
                    "description": "Converted YOLO dataset",
                    "version": "1.0",
                    "year": 2025,
                },
                "licenses": [],
                "images": [],
                "annotations": [],
                "categories": [
                    {"id": i, "name": name} for i, name in enumerate(class_names)
                ],
            }

            annotation_id = 1
            for image_id, image_file in enumerate(
                tqdm(os.listdir(image_dir), desc="Converting YOLO to COCO")
            ):
                if not image_file.lower().endswith(
                    (".png", ".jpg", ".jpeg", ".bmp", ".tiff")
                ):
                    continue  # Skip non-image files

                # Add image info to COCO
                image_path = os.path.join(image_dir, image_file)
                image_width, image_height = Image.open(image_path).size
                coco_data["images"].append(
                    {
                        "id": image_id,
                        "file_name": image_file,
                        "width": image_width,
                        "height": image_height,
                    }
                )

                # Copy image to COCO images directory
                dst_image_path = os.path.join(output_dir, image_file)
                shutil.copy(image_path, dst_image_path)

                # Process corresponding YOLO label file
                label_file_path = os.path.join(
                    yolo_dir, "labels", f"{Path(image_file).stem}.txt"
                )
                if not os.path.exists(label_file_path):
                    print(f"Warning: Label file {label_file_path} not found. Skipping.")
                    continue

                with open(label_file_path, "r") as label_file:
                    for line in label_file:
                        class_id, x_center, y_center, width, height = map(
                            float, line.strip().split()
                        )
                        x_min = (x_center - width / 2) * image_width
                        y_min = (y_center - height / 2) * image_height
                        width *= image_width
                        height *= image_height

                        # Add annotation to COCO
                        coco_data["annotations"].append(
                            {
                                "id": annotation_id,
                                "image_id": image_id,
                                "category_id": int(class_id),
                                "bbox": [x_min, y_min, width, height],
                                "area": width * height,
                                "iscrowd": 0,
                            }
                        )
                        annotation_id += 1

            # Save COCO annotations to file
            with open(output_file, "w") as f:
                json.dump(coco_data, f, indent=4)

            print(
                f"YOLO to COCO conversion completed. COCO annotations saved to {output_file}"
            )

        except Exception as e:
            print(f"Error during YOLO to COCO conversion: {e}")

    def yolo_to_pascalvoc(self, yolo_dir: str, output_dir: str, image_dir: str):
        """
        Convert a YOLO dataset to PASCAL VOC format and rearrange images.
        Args:
            yolo_dir (str): Path to the YOLO labels directory.
            output_dir (str): Directory to save the PASCAL VOC-formatted dataset.
            image_dir (str): Directory containing the images referenced in the YOLO dataset.

        classlist: ensure the classlist is in the the same folder as the yolo_dir
        """
        try:
            annotations_dir = os.path.join(output_dir, "Annotations")
            images_dir = os.path.join(output_dir, "JPEGImages")
            os.makedirs(annotations_dir, exist_ok=True)
            os.makedirs(images_dir, exist_ok=True)

            classes_file = os.path.join(yolo_dir, "classes.txt")
            with open(classes_file, "r") as f:
                class_names = [line.strip() for line in f.readlines()]

            for image_file in tqdm(
                os.listdir(image_dir), desc="Converting YOLO to PASCAL VOC"
            ):
                if not image_file.lower().endswith((".png", ".jpg", ".jpeg")):
                    continue

                image_path = os.path.join(image_dir, image_file)
                image_width, image_height = Image.open(image_path).size

                dst_image_path = os.path.join(images_dir, image_file)
                shutil.copy(image_path, dst_image_path)

                label_file_path = os.path.join(
                    yolo_dir, "labels", f"{Path(image_file).stem}.txt"
                )
                if not os.path.exists(label_file_path):
                    print(f"Warning: Label file {label_file_path} not found. Skipping.")
                    continue

                annotation_file_path = os.path.join(
                    annotations_dir, f"{Path(image_file).stem}.xml"
                )
                annotation = ET.Element("annotation")
                ET.SubElement(annotation, "folder").text = "JPEGImages"
                ET.SubElement(annotation, "filename").text = image_file
                ET.SubElement(annotation, "path").text = dst_image_path

                size = ET.SubElement(annotation, "size")
                ET.SubElement(size, "width").text = str(image_width)
                ET.SubElement(size, "height").text = str(image_height)
                ET.SubElement(size, "depth").text = "3"

                with open(label_file_path, "r") as label_file:
                    for line in label_file:
                        class_id, x_center, y_center, width, height = map(
                            float, line.strip().split()
                        )
                        x_min = int((x_center - width / 2) * image_width)
                        y_min = int((y_center - height / 2) * image_height)
                        x_max = int((x_center + width / 2) * image_width)
                        y_max = int((y_center + height / 2) * image_height)

                        obj = ET.SubElement(annotation, "object")
                        ET.SubElement(obj, "name").text = class_names[int(class_id)]
                        ET.SubElement(obj, "pose").text = "Unspecified"
                        ET.SubElement(obj, "truncated").text = "0"
                        ET.SubElement(obj, "difficult").text = "0"

                        bndbox = ET.SubElement(obj, "bndbox")
                        ET.SubElement(bndbox, "xmin").text = str(x_min)
                        ET.SubElement(bndbox, "ymin").text = str(y_min)
                        ET.SubElement(bndbox, "xmax").text = str(x_max)
                        ET.SubElement(bndbox, "ymax").text = str(y_max)

                tree = ET.ElementTree(annotation)
                tree.write(annotation_file_path)

            print(
                f"YOLO to PASCAL VOC conversion completed. Dataset saved to {output_dir}"
            )

        except Exception as e:
            print(f"Error during YOLO to PASCAL VOC conversion: {e}")

    def pascalvoc_to_yolo(self, pascalvoc_dir: str, output_dir: str, image_dir: str):
        """
        Convert a PASCAL VOC dataset to YOLO format and rearrange images.

        Args:
            pascalvoc_dir (str): Path to the PASCAL VOC Annotations directory (XML files).
            output_dir (str): Directory to save the YOLO-formatted dataset.
            image_dir (str): Directory containing the images referenced in the PASCAL VOC dataset.
        """
        try:
            # Ensure output directories exist
            labels_dir = os.path.join(output_dir, "labels")
            images_dir = os.path.join(output_dir, "images")
            os.makedirs(labels_dir, exist_ok=True)
            os.makedirs(images_dir, exist_ok=True)

            # Extract class names from the PASCAL VOC annotations
            class_names = set()

            for annotation_file in tqdm(
                os.listdir(pascalvoc_dir), desc="Processing PASCAL VOC Annotations"
            ):
                if not annotation_file.endswith(".xml"):
                    continue

                annotation_path = os.path.join(pascalvoc_dir, annotation_file)
                tree = ET.parse(annotation_path)
                root = tree.getroot()

                # Extract class names and add to the set
                for obj in root.findall("object"):
                    class_name = obj.find("name").text
                    class_names.add(class_name)

            # Save class names to a YOLO classes.txt file
            class_names = sorted(class_names)  # Sort class names alphabetically
            class_name_to_id = {name: idx for idx, name in enumerate(class_names)}
            with open(os.path.join(output_dir, "classes.txt"), "w") as class_file:
                for class_name in class_names:
                    class_file.write(f"{class_name}\n")

            # Process each annotation file and convert to YOLO format
            for annotation_file in tqdm(
                os.listdir(pascalvoc_dir), desc="Converting PASCAL VOC to YOLO"
            ):
                if not annotation_file.endswith(".xml"):
                    continue

                annotation_path = os.path.join(pascalvoc_dir, annotation_file)
                tree = ET.parse(annotation_path)
                root = tree.getroot()

                # Get image file name and dimensions
                image_filename = root.find("filename").text
                image_path = os.path.join(image_dir, image_filename)
                if not os.path.exists(image_path):
                    print(f"Warning: Image {image_path} not found. Skipping.")
                    continue

                image_width = int(root.find("size/width").text)
                image_height = int(root.find("size/height").text)

                # Copy image to YOLO images directory
                dst_image_path = os.path.join(images_dir, image_filename)
                shutil.copy(image_path, dst_image_path)

                # Create YOLO label file
                label_file_path = os.path.join(
                    labels_dir, f"{Path(image_filename).stem}.txt"
                )
                with open(label_file_path, "w") as label_file:
                    for obj in root.findall("object"):
                        class_name = obj.find("name").text
                        class_id = class_name_to_id[class_name]

                        bndbox = obj.find("bndbox")
                        x_min = int(bndbox.find("xmin").text)
                        y_min = int(bndbox.find("ymin").text)
                        x_max = int(bndbox.find("xmax").text)
                        y_max = int(bndbox.find("ymax").text)

                        # Convert to YOLO format: [class_id, x_center, y_center, width, height]
                        x_center = ((x_min + x_max) / 2) / image_width
                        y_center = ((y_min + y_max) / 2) / image_height
                        width = (x_max - x_min) / image_width
                        height = (y_max - y_min) / image_height

                        # Write YOLO annotation
                        label_file.write(
                            f"{class_id} {x_center} {y_center} {width} {height}\n"
                        )

            print(
                f"PASCAL VOC to YOLO conversion completed. YOLO dataset saved to {output_dir}"
            )

        except Exception as e:
            print(f"Error during PASCAL VOC to YOLO conversion: {e}")

    def coco_to_pascalvoc(self, coco_path: str, output_dir: str, image_dir: str):
        """
        Convert a COCO dataset to PASCAL VOC format and rearrange images.

        Args:
            coco_path (str): Path to the COCO annotations file (e.g., _annotations.coco.json).
            output_dir (str): Directory to save the PASCAL VOC-formatted dataset.
            image_dir (str): Directory containing the images referenced in the COCO dataset.
        """
        try:
            annotations_dir = os.path.join(output_dir, "Annotations")
            images_dir = os.path.join(output_dir, "JPEGImages")
            os.makedirs(annotations_dir, exist_ok=True)
            os.makedirs(images_dir, exist_ok=True)

            # Load COCO annotations
            with open(coco_path, "r") as f:
                coco_data = json.load(f)

            categories = {
                category["id"]: category["name"] for category in coco_data["categories"]
            }

            for image in tqdm(
                coco_data["images"], desc="Converting COCO to PASCAL VOC"
            ):
                image_id = image["id"]
                image_filename = image["file_name"]
                image_width = image["width"]
                image_height = image["height"]

                src_image_path = os.path.join(image_dir, image_filename)
                dst_image_path = os.path.join(images_dir, image_filename)
                if not os.path.exists(src_image_path):
                    print(f"Warning: Image {src_image_path} not found. Skipping.")
                    continue
                shutil.copy(src_image_path, dst_image_path)

                annotation_file_path = os.path.join(
                    annotations_dir, f"{Path(image_filename).stem}.xml"
                )
                annotation = ET.Element("annotation")
                ET.SubElement(annotation, "folder").text = "JPEGImages"
                ET.SubElement(annotation, "filename").text = image_filename
                ET.SubElement(annotation, "path").text = dst_image_path

                size = ET.SubElement(annotation, "size")
                ET.SubElement(size, "width").text = str(image_width)
                ET.SubElement(size, "height").text = str(image_height)
                ET.SubElement(size, "depth").text = "3"

                for annotation_data in coco_data["annotations"]:
                    if annotation_data["image_id"] == image_id:
                        category_id = annotation_data["category_id"]
                        bbox = annotation_data[
                            "bbox"
                        ]  # COCO format: [x_min, y_min, width, height]

                        x_min = int(bbox[0])
                        y_min = int(bbox[1])
                        x_max = int(bbox[0] + bbox[2])
                        y_max = int(bbox[1] + bbox[3])

                        obj = ET.SubElement(annotation, "object")
                        ET.SubElement(obj, "name").text = categories[category_id]
                        ET.SubElement(obj, "pose").text = "Unspecified"
                        ET.SubElement(obj, "truncated").text = "0"
                        ET.SubElement(obj, "difficult").text = "0"

                        bndbox = ET.SubElement(obj, "bndbox")
                        ET.SubElement(bndbox, "xmin").text = str(x_min)
                        ET.SubElement(bndbox, "ymin").text = str(y_min)
                        ET.SubElement(bndbox, "xmax").text = str(x_max)
                        ET.SubElement(bndbox, "ymax").text = str(y_max)

                tree = ET.ElementTree(annotation)
                tree.write(annotation_file_path)

            print(
                f"COCO to PASCAL VOC conversion completed. Dataset saved to {output_dir}"
            )

        except Exception as e:
            print(f"Error during COCO to PASCAL VOC conversion: {e}")

    def pascalvoc_to_coco(self, pascalvoc_dir: str, output_file: str, image_dir: str):
        """
        Convert a PASCAL VOC dataset to COCO format and rearrange images.

        Args:
            pascalvoc_dir (str): Path to the PASCAL VOC Annotations directory (XML files).
            output_file (str): Path to save the COCO annotations file.
            image_dir (str): Directory containing the images referenced in the PASCAL VOC dataset.
        """
        try:
            output_dir = os.path.dirname(output_file)

            os.makedirs(output_dir, exist_ok=True)

            coco_data = {
                "info": {
                    "description": "Converted PASCAL VOC dataset",
                    "version": "1.0",
                    "year": 2025,
                },
                "licenses": [],
                "images": [],
                "annotations": [],
                "categories": [],
            }

            class_names = set()
            annotation_id = 1

            for annotation_file in tqdm(
                os.listdir(pascalvoc_dir), desc="Processing PASCAL VOC Annotations"
            ):
                if not annotation_file.endswith(".xml"):
                    continue

                annotation_path = os.path.join(pascalvoc_dir, annotation_file)
                tree = ET.parse(annotation_path)
                root = tree.getroot()

                image_filename = root.find("filename").text
                image_path = os.path.join(image_dir, image_filename)
                if not os.path.exists(image_path):
                    print(f"Warning: Image {image_path} not found. Skipping.")
                    continue

                image_width = int(root.find("size/width").text)
                image_height = int(root.find("size/height").text)

                dst_image_path = os.path.join(output_dir, image_filename)
                shutil.copy(image_path, dst_image_path)

                image_id = len(coco_data["images"])
                coco_data["images"].append(
                    {
                        "id": image_id,
                        "file_name": image_filename,
                        "width": image_width,
                        "height": image_height,
                    }
                )

                for obj in root.findall("object"):
                    class_name = obj.find("name").text
                    class_names.add(class_name)

                    bndbox = obj.find("bndbox")
                    x_min = int(bndbox.find("xmin").text)
                    y_min = int(bndbox.find("ymin").text)
                    x_max = int(bndbox.find("xmax").text)
                    y_max = int(bndbox.find("ymax").text)

                    width = x_max - x_min
                    height = y_max - y_min

                    coco_data["annotations"].append(
                        {
                            "id": annotation_id,
                            "image_id": image_id,
                            "category_id": class_name,
                            "bbox": [x_min, y_min, width, height],
                            "area": width * height,
                            "iscrowd": 0,
                        }
                    )
                    annotation_id += 1

            # Add categories to COCO
            class_names = sorted(class_names)
            coco_data["categories"] = [
                {"id": idx, "name": name} for idx, name in enumerate(class_names)
            ]

            # Save COCO annotations to file
            with open(output_file, "w") as f:
                json.dump(coco_data, f, indent=4)

            print(
                f"PASCAL VOC to COCO conversion completed. COCO annotations saved to {output_file}"
            )

        except Exception as e:
            print(f"Error during PASCAL VOC to COCO conversion: {e}")


# Wrapper functions for direct imports
def coco_to_yolo(coco_path: str, output_dir: str, image_dir: str):
    converter = DatasetConverter()
    converter.coco_to_yolo(coco_path, output_dir, image_dir)


def yolo_to_coco(yolo_dir: str, output_file: str, image_dir: str):
    converter = DatasetConverter()
    converter.yolo_to_coco(yolo_dir, output_file, image_dir)


def yolo_to_pascalvoc(yolo_dir: str, output_dir: str, image_dir: str):
    converter = DatasetConverter()
    converter.yolo_to_pascalvoc(yolo_dir, output_dir, image_dir)


def pascalvoc_to_yolo(pascalvoc_dir: str, output_dir: str, image_dir: str):
    converter = DatasetConverter()
    converter.pascalvoc_to_yolo(pascalvoc_dir, output_dir, image_dir)


def coco_to_pascalvoc(coco_path: str, output_dir: str, image_dir: str):
    converter = DatasetConverter()
    converter.coco_to_pascalvoc(coco_path, output_dir, image_dir)


def pascalvoc_to_coco(pascalvoc_dir: str, output_file: str, image_dir: str):
    converter = DatasetConverter()
    converter.pascalvoc_to_coco(pascalvoc_dir, output_file, image_dir)
