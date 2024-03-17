import os
import xml.etree.ElementTree as ET
from collections import Counter

def count_labels_in_xml(path):
    label_list = []
    for file_or_dir in os.listdir(path):
        full_path = os.path.join(path, file_or_dir)
        if os.path.isdir(full_path):
            for xml_file in os.listdir(full_path):
                if xml_file.endswith('.xml'):
                    xml_file_path = os.path.join(full_path, xml_file)
                    root = ET.parse(xml_file_path).getroot()
                    for label_element in root.findall('object'):
                        label = label_element.find('name').text
                        label_list.append(label)
    label_counter = Counter(label_list)
    for label, count in label_counter.items():
        print('{} : {}'.format(label, count))


# Example usage
# path_to_xml_files = "data/xml_labels"
# count_labels_in_xml(path_to_xml_files)

