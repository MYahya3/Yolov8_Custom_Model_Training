import shutil
import os
import xml.etree.ElementTree as ET

import os
import xml.etree.ElementTree as ET

def convert_coordinates(size, box):
    dw, dh = 1.0 / size[0], 1.0 / size[1]
    x, y = (box[0] + box[1]) / 2.0, (box[2] + box[3]) / 2.0
    w, h = box[1] - box[0], box[3] - box[2]
    return x * dw, y * dh, w * dw, h * dh

def xml_to_yolo(xml_file, classes):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    image_name = root.find('filename').text
    image_width = int(root.find('size/width').text)
    image_height = int(root.find('size/height').text)

    labels = []
    for obj in root.findall('object'):
        cls = obj.find('name').text
        if cls in classes:
            cls_id = classes.index(cls)
            xml_box = obj.find('bndbox')
            box = [float(xml_box.find(tag).text) for tag in ['xmin', 'xmax', 'ymin', 'ymax']]
            bb = convert_coordinates((image_width, image_height), box)
            labels.append(f"{cls_id} {' '.join(map(str, bb))}")

    return image_name, labels

def save_yolo_format(image_name, labels, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    yolo_file_path = os.path.join(output_dir, os.path.splitext(image_name)[0] + '.txt')
    with open(yolo_file_path, 'w') as yolo_file:
        yolo_file.write('\n'.join(labels))

def convert_folder(xml_folder, output_folder, classes):
    os.makedirs(output_folder, exist_ok=True)
    for root, _, files in os.walk(xml_folder):
        for file in files:
            if file.endswith('.xml'):
                xml_file_path = os.path.join(root, file)
                image_name, labels = xml_to_yolo(xml_file_path, classes)
                output_subfolder = os.path.join(output_folder, os.path.relpath(root, xml_folder))
                save_yolo_format(image_name, labels, output_subfolder)

if __name__ == "__main__":
    xml_directory = r'data/xml_labels'
    output_directory = r'data/yolo_labels'
    classes = ['cat','dog', 'monkey']

    convert_folder(xml_directory, output_directory, classes)
