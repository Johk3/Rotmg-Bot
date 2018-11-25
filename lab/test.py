from time import sleep
import pyautogui
import mss
import cv2
import mss.tools
import time
import numpy as np
from os import walk
import imutils
from analyzer import ColorLabeler
import keyboard
from random import randint
import matplotlib.pylab as plt
from PIL import Image
from lab.tradeanalyzer import Main
from collections import Counter
import os, shutil
from collections import defaultdict

# with mss.mss() as sct:
#     monitor = {"top": 480, "left": 1160, "width": 100, "height": 40}
#     img = sct.grab(monitor)
#     mss.tools.to_png(img.rgb, img.size, output="tradeconfirmation.png")
#     im = Image.open("tradeconfirmation.png")
#     pix = im.load()
#     for i in range(im.size[0]):
#         if i >= 39:
#             color = pix[i, 39]
#             print(color)
#             if color[0] == 113 and color[1] == 139 and color[2] == 80:
#                 print(True)
#         else:
#             color = pix[i, i]
#             print(color)
#             if color[0] == 113 and color[1] == 139 and color[2] == 80:
#                 print(True)
#
# mouseX = 1161
# mousex = 1312
# mouseY = 685
# offsetX = 13
# offsetY = 10
#
# mousex = 1312
# mouseY = 685
# offsetX = 50
# offsetY = 10
# mouseX = 1161
#
# sleep(2)
# pyautogui.keyDown('w')
# sleep(2)
# pyautogui.keyUp('w')
# quit = False
# while not quit:
#     with mss.mss() as sct:
#         pyautogui.keyDown('d')
#         sleep(0.01)
#         pyautogui.keyUp('d')
#         monitor = {"top": 662, "left": 1232, "width": 70, "height": 34}
#         img = sct.grab(monitor)
#         mss.tools.to_png(img.rgb, img.size, output="vault.png")
#         file = "vault.png"
#         img = Image.open(file)
#         colors = img.getcolors(256)
#         max_occurence, most_present = 0, 0
#         check = 0
#         try:
#             for c in colors:
#                 if c[0] > max_occurence:
#                     (max_occurence, most_present) = c
#             for value in most_present:
#                 if value == 255:
#                     check += 1
#             if check == 3:
#                 quit = True
#         except TypeError:
#             pass
#
# pyautogui.moveTo(mouseX, mouseY)
# pyautogui.moveTo(mousex - offsetX, mouseY - offsetY, 1)
# pyautogui.click(1325 - offsetX, 675)
# sleep(8)
# pyautogui.keyDown('w')
# sleep(0.2)
# pyautogui.keyUp('w')

with mss.mss() as sct:
    monitor = {"top": 600, "left": 1160, "width": 197, "height": 114}
    found_spots = defaultdict(list)

    sct_image = sct.grab(monitor)
    mss.tools.to_png(sct_image.rgb, sct_image.size, output="invault.png")

    imgpath = "invault.png"

    # load the image and resize it to a smaller factor so that
    # the shapes can be approximated better
    image = cv2.imread(imgpath)
    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])

    # blur the resized image slightly, then convert it to both
    # grayscale and the L*a*b* color spaces
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
    thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

    # find contours in the thresholded image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # initialize the shape detector and color labeler
    cl = ColorLabeler()
    i = 0
    for c in cnts:
        # compute the center of the contour
        if i >= 1 and i <= 8:
            M = cv2.moments(c)
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)

            # detect the shape of the contour and label the color
            color = cl.label(lab, c, True)

            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then draw the contours and the name of the shape and labeled
            # color on the image
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")
            text = "{}".format(color)
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.putText(image, text, (cX - 15, cY - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

            # show the output image
            cv2.imshow("Image", image)
            if color != None:
                if color == "empty":
                    found_spots[color].append([cX, cY])
            print(found_spots["empty"][0][0])
        i += 1


