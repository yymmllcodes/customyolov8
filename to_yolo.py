import os
import json
import xml.etree.ElementTree as ET

def normalize_coordinates(points, img_width, img_height):
    """Normalize the coordinates to be between 0 and 1."""
    return [(x / img_width, y / img_height) for x, y in points]

def convert_annotation_to_yolo(json_file_path, output_dir):
    """Convert the annotation file to YOLO format."""
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    img_width = data['image_width']
    img_height = data['image_height']
    
    shapes = data['annotations']
    
    # Prepare the output file path
    output_file_path = os.path.join(output_dir, os.path.splitext(os.path.basename(json_file_path))[0] + '.txt')
    
    with open(output_file_path, 'w') as out_file:
        for shape in shapes:
            label = shape['label']
            class_index = 0  # todo Replace with appropriate class index or mapping
            points = shape['segmentation']
            normalized_points = normalize_coordinates(points, img_width, img_height)
            points_str = ' '.join([f"{x} {y}" for x, y in normalized_points])
            out_file.write(f"{class_index} {points_str}\n")

def process_directory(input_dir, output_dir):
    """Process all annotation files in the directory and convert them to YOLO format."""
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):  # Adjust extension based on your annotation file format
            json_file_path = os.path.join(input_dir, filename)
            convert_annotation_to_yolo(json_file_path, output_dir)

# Example usage
input_dir = 'path/to/your/annotation/directory'
output_dir = 'path/to/your/output/directory'
process_directory(input_dir, output_dir)
