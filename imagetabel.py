# -*- coding: utf-8 -*-
# License: Anti-996, Anti-995, Follow-955 (ignore if the license is not exist)
# recommand using miniconda
# conda install pillow numpy opencv -c conda-forge -y
from __future__ import print_function

import cv2
from PIL import Image
import io
import numpy as np
try:
    import urllib.request as urllib
except ModuleNotFoundError:
    import urllib

# read an image by filepath or image_url, im=filepath/image_url
def imgread(im):
    try:
        image = Image.open(io.BytesIO(urllib.urlopen(im).read()))
    except ValueError:
        try:
            image = Image.open(im)
        except FileExistsError:
            return None
    try:
        image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    except:
        return None
    return image

# your image filepath or url
img = "https://cbu01.alicdn.com/img/ibank/2019/115/186/10753681511_1065342506.jpg"

im = imgread(img)

# cv2.imshow('image', im)
# cv2.waitKey(0)

im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
# cv2.imshow("gray image", im)
# cv2.waitKey(0)

dst = cv2.adaptiveThreshold(~im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -2)

# cv2.imshow("binary image", dst)
# cv2.waitKey(0)

# copy dst, then for horizontal and vertical lines' detection.
horizontal = dst.copy()
vertical = dst.copy()
scale = 15  # play with this variable in order to increase/decrease the amount of lines to be detected

# Specify size on horizontal axis
print(horizontal.shape)
horizontalsize = horizontal.shape[1] // scale
horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize, 1))
horizontal = cv2.erode(horizontal, horizontalStructure, (-1, -1))
horizontal = cv2.dilate(horizontal, horizontalStructure, (-1, -1))
cv2.imshow("horizontal line", horizontal)
cv2.waitKey(0)

# vertical
verticalsize = vertical.shape[0] // scale
verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
vertical = cv2.erode(vertical, verticalStructure, (-1, -1))
vertical = cv2.dilate(vertical, verticalStructure, (-1, -1))
cv2.imshow("horizontal line", vertical)
cv2.waitKey(0)

# table line
table = horizontal + vertical
cv2.imshow("table", table)
cv2.waitKey(0)

# the joint points between horizontal line and vertical line.
joints = cv2.bitwise_and(horizontal, vertical)
cv2.imshow("joint points", joints)
cv2.waitKey(0)
