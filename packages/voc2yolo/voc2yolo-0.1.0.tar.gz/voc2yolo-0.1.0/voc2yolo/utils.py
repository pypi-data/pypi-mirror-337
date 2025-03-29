import os

def save_yolo_annotations(yolo_data, output_path):
    """
    Saves YOLO annotations to a text file.

    Args:
        yolo_data (list): List of YOLO annotations as strings.
        output_path (str): File path to save the annotations.
    """
    with open(output_path, "w") as f:
        f.write("\n".join(yolo_data))