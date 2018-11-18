# -*- coding: utf-8 -*-
import cv2
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import os
import glob

if __name__ == '__main__':

    # img = cv2.imread('../data/0006R0_f00930.png')
    # bbox_path = '../data/0006R0_f00930.xml'

    root = os.path.expanduser('~/Data/CamVid')
    split = 'train'
    # print('root:', root)
    file_list = glob.glob(root + '/' + split + '/*.png')
    file_list.sort()
    print(file_list)


    bbox_width = 960
    bbox_height = 720
    img_width = 480
    img_height = 360

    for img_name in file_list:
        object_det_bboxes = []
        # print(img_name)
        img_file_name = img_name[img_name.rfind('/')+1:img_name.rfind('.')]
        img_path = root + '/' + split + '/' + img_file_name + '.png'
        lbl_path = root + '/' + split + 'annot/' + img_file_name + '.png'
        bbox_path = root + '/' + split + 'bbox/' + img_file_name + '.xml'

        img = cv2.imread(img_path)

        if os.path.exists(bbox_path):
            print(bbox_path)
            bbox_tree = ET.parse(bbox_path)
            bbox_root = bbox_tree.getroot()

            for bbox_obj in bbox_root.findall('object'):
                bbox_obj_name = bbox_obj.find('name').text
                # if bbox_obj_name not in ['Car']:
                #     continue
                bbox_obj_bndbox = bbox_obj.find('bndbox')
                xmin = int(int(bbox_obj_bndbox.find('xmin').text) * 1.0 / bbox_width * img_width)
                ymin = int(int(bbox_obj_bndbox.find('ymin').text) * 1.0 / bbox_height * img_height)
                xmax = int(int(bbox_obj_bndbox.find('xmax').text) * 1.0 / bbox_width * img_width)
                ymax = int(int(bbox_obj_bndbox.find('ymax').text) * 1.0 / bbox_height * img_height)
                print bbox_obj_name, xmin, ymin, xmax, ymax
                object_det_bboxes.append([xmin, ymin, xmax, ymax, 0])

        for object_det_bbox in object_det_bboxes:
            xmin = object_det_bbox[0]
            ymin = object_det_bbox[1]
            xmax = object_det_bbox[2]
            ymax = object_det_bbox[3]
            cv2.rectangle(img, pt1=(xmin, ymin), pt2=(xmax, ymax), color=(255, 0, 0), thickness=1)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imshow('img', img)
        cv2.waitKey(30)
        # plt.imshow(img)
        # plt.show()
