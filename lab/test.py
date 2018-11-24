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

with mss.mss() as sct:
    monitor = {"top": 480, "left": 1160, "width": 100, "height": 40}
    img = sct.grab(monitor)
    mss.tools.to_png(img.rgb, img.size, output="tradeconfirmation.png")
    im = Image.open("tradeconfirmation.png")
    pix = im.load()
    for i in range(im.size[0]):
        if i >= 39:
            color = pix[i, 39]
            print(color)
            if color[0] == 113 and color[1] == 139 and color[2] == 80:
                print(True)
        else:
            color = pix[i, i]
            print(color)
            if color[0] == 113 and color[1] == 139 and color[2] == 80:
                print(True)

