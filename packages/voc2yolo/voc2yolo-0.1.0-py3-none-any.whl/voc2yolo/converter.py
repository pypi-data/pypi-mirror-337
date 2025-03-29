import xml.etree.ElementTree as ET
import os

def parse_voc_xml(xml_file):
    """
    Parses a Pascal VOC XML annotation file and extracts image size and object details.

    Args:
        xml_file (str): Path to the XML file.

    Returns:
        dict: A dictionary containing image width, height, and object annotations.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract image size
    size = root.find("size")
    img_width = int(size.find("width").text)
    img_height = int(size.find("height").text)

    objects = []
    for obj in root.findall("object"):
        label = obj.find("name").text
        bbox = obj.find("bndbox")
        xmin = int(bbox.find("xmin").text)
        ymin = int(bbox.find("ymin").text)
        xmax = int(bbox.find("xmax").text)
        ymax = int(bbox.find("ymax").text)

        objects.append({"label": label, "bbox": (xmin, ymin, xmax, ymax)})

    return {"width": img_width, "height": img_height, "objects": objects}

def convert_bbox_voc_to_yolo(img_width, img_height, xmin, ymin, xmax, ymax):
    """
    Converts Pascal VOC bounding box format to YOLO format.

    Args:
        img_width (int): Width of the image.
        img_height (int): Height of the image.
        xmin (int): Top-left x-coordinate.
        ymin (int): Top-left y-coordinate.
        xmax (int): Bottom-right x-coordinate.
        ymax (int): Bottom-right y-coordinate.

    Returns:
        tuple: (x_center, y_center, width, height) in YOLO format.
    """
    x_center = ((xmin + xmax) / 2) / img_width
    y_center = ((ymin + ymax) / 2) / img_height
    width = (xmax - xmin) / img_width
    height = (ymax - ymin) / img_height

    return (x_center, y_center, width, height)

def convert_voc_to_yolo(xml_file, class_mapping):
    """
    Converts a Pascal VOC XML annotation file to YOLO format.

    Args:
        xml_file (str): Path to the XML file.
        class_mapping (dict): Dictionary mapping class names to class IDs.

    Returns:
        list: YOLO-formatted annotation lines.
    """
    voc_data = parse_voc_xml(xml_file)
    yolo_annotations = []

    for obj in voc_data["objects"]:
        label = obj["label"]
        if label not in class_mapping:
            continue  # Skip unknown classes

        class_id = class_mapping[label]
        bbox = convert_bbox_voc_to_yolo(voc_data["width"], voc_data["height"], *obj["bbox"])
        yolo_annotations.append(f"{class_id} " + " ".join(map(str, bbox)))

    return yolo_annotations