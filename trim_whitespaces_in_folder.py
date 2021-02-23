#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script reads a bunch of images of same dimension from a folder and
find the largest whitespace crop dimensions for the whole set and applies it
to all the images.
"""
from __future__ import print_function
import cv2
import glob
import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This is the simple VSLAM pipeline')
    parser.add_argument('-f', '--folder', help='folder where all the images are',
                        default=os.path.curdir)
    parser.add_argument('-e', '--ext', help='extensions of image files', nargs='+',
                        default=['png'])
    parser.add_argument('-d', '--dry', help='dry run, report trim value but not modify files',
                         action='store_true')
    parser.add_argument('-p', '--padding', type=int, help='Extra padding in pixels around crop area',
                         default=0)

    args = parser.parse_args()

    extensions = args.ext
    extensions = [e.upper() for e in extensions] + [e.lower() for e in extensions]
    dryrun = args.dry
    folder = os.path.abspath(args.folder)
    padding = 0;
    print("Working on folder: {}".format(folder))
    print("Exts: ",extensions)
    print("Padding set to {:d}".format(padding))

    image_names = []
    for ext in extensions:
        image_names = image_names + glob.glob(folder+'/*.'+ext)

    images = []
    heights = []
    widths = []
    x1s=[]; y1s=[]; x2s=[]; y2s=[]
    for image_name in image_names:
        img = cv2.imread(image_name)
        images.append(img)
        heights.append(img.shape[0])
        widths.append(img.shape[1])

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_img_inv = cv2.bitwise_not(gray_img)
        coords = cv2.findNonZero(gray_img_inv) # Find all non-zero points (text)
        x, y, w, h = cv2.boundingRect(coords) # Find min
        x1s.append(x)
        y1s.append(y)
        x2s.append(x+w)
        y2s.append(y+h)

    x1_crop = min(x1s)-padding
    x2_crop = max(x2s)+padding
    y1_crop = min(y1s)-padding
    y2_crop = max(y2s)+padding

    assert max(heights) == min(heights)
    assert max(widths) == min(widths)
    
    print("Image dimensions: width x height: {:d} x {:d}".format(widths[0], heights[0]))
    print("Valid crop limits x:{:d} to {:d}, y:{:d} to {:d}".format(x1_crop,x2_crop,y1_crop,y2_crop))
    print("Valid crop numpy indices [rows,cols]:[{:d} : -{:d}, {:d} : -{:d}]".format(y1_crop,heights[0]-y2_crop, x1_crop, widths[0]-x2_crop))
    
    if dryrun:
        print("This was a dry run")
        
    else:
        for image_name, img in zip(image_names, images):
            img_name_base, img_name_ext = os.path.splitext(image_name)
            img_name_out = img_name_base + '_trim' + img_name_ext
    
            img_cropped = img[y1_crop:y2_crop, x1_crop:x2_crop]
    
            if img_name_ext == '.png' or img_name_ext == '.PNG':
                cv2.imwrite(img_name_out, img_cropped, [cv2.IMWRITE_PNG_COMPRESSION, 9])