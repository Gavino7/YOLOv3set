
import re
import os, argparse
import xml.etree.ElementTree as ET
#from tqdm import tqdm
from collections import OrderedDict

file_ann = open("annotations.txt", "w")
class_map = {name: idx for idx, name in enumerate(
		open('classes.txt').read().splitlines())}
for f in os.listdir('xmlannotation'):
    file=os.path.join('xmlannotation',f)
    if f.endswith(".xml"):

        in_file = open(file, encoding ='utf-8')
        tree = ET.parse(in_file)
        root = tree.getroot()


        bboxes = []

        for obj in root.iter('object'):

            xml_box = obj.find('bndbox')
            bbox = xml_box.find('xmin').text + ',' + xml_box.find('ymin').text + ',' + xml_box.find('xmax').text + ',' + xml_box.find('ymax').text + ',' + str(class_map[obj.find('name').text])
            bboxes.append(bbox)

        row = os.path.join('test_images',f.split('.')[0]+'.jpg') + ' ' + ' '.join(bboxes) + '\n'
        print(row)
        file_ann.write(row)

file_ann.close()
