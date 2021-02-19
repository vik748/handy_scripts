#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 12:34:49 2021

@author: vik748
"""
from __future__ import print_function
import cv2
import glob
import os
import argparse

image_list = []
for filename in glob.glob('yourpath/*.gif'): #assuming gif
    im=Image.open(filename)
    image_list.append(im)

#if __name__ == '__main__':
    # passing arguments from the terminal
parser = argparse.ArgumentParser(description='This is the simple VSLAM pipeline')
parser.add_argument('-f', '--folder', help='folder where all the images are',
                    default=os.path.curdir)
parser.add_argument('-e', '--ext', help='extensions of image files', nargs='+',
                    default=['png'])    

args = parser.parse_args()

extensions = args.ext
extensions = [e.upper() for e in extensions] + [e.lower() for e in extensions]
folder = os.path.abspath(args.folder)
print("Working on folder: {}".format(folder))
print("Exts: ",extensions)

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

x1_crop = min(x1s)
x2_crop = max(x2s)
y1_crop = min(y1s)
y2_crop = max(y2s)
    
assert max(heights) == min(heights)
assert max(widths) == min(widths)
  
for image_name, img in zip(image_names, images):
    img_name_base, img_name_ext = os.path.splitext(image_name)
    img_name_out = img_name_base + '_trim' + img_name_ext
    
    img_cropped = img[y1_crop:y2_crop, x1_crop:x2_crop]
    
    if img_name_ext == '.png' or img_name_ext == '.PNG':
        cv2.imwrite(img_name_out, img_cropped, [cv2.IMWRITE_PNG_COMPRESSION, 9]) # Save the image
    
