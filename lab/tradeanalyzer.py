import cv2 as cv
# import numpy as np
# from scipy.spatial import distance as dist
# from collections import OrderedDict
import numpy as np
# import cv2
from PIL import Image
# from os import walk
# import imutils


class Main:
    def __init__(self):
        self.potions = {}

    def run(self, img, template):
        im = Image.open(template)
        img_rgb = cv.imread(template)
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        template = cv.imread(img,0)
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        location = []
        i = 0
        for pt in zip(*loc[::-1]):
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            location.append(pt)
            location.append((pt[0] + w, pt[1] + h))
            crop_rectangle = pt[0], pt[1], pt[0] + w, pt[1] + h
            cropped_im = im.crop(crop_rectangle)
            cropped_im.save("lab/trade_potions/potion{}.png".format(i))
            i += 1
        cv.imwrite("res.png", img_rgb)
        return location

    def scan(self, file):
        im = Image.open(file)
        pix = im.load()
        for i in range(im.size[0]):
            color = pix[i, i]

            if color[0] == 67 and color[1] == 140 and color[2] == 247:
                return "wisdom"
            if color[0] == 60 and color[1] == 223 and color[2] == 123:
                return "speed"
            if color[0] == 216 and color[1] == 85 and color[2] == 235:
                return "attack"
            if color[0] == 229 and color[1] == 198 and color[2] == 83:
                return "mana"
            if color[0] == 56 and color[1] == 212 and color[2] == 218:
                return "life"
            if color[0] == 225 and color[1] == 127 and color[2] == 39:
                return "vitdex"
            if color[0] == 201 and color[1] == 0 and color[2] == 26:
                return "vitdex"
            if color[0] == 9 and color[1] == 8 and color[2] == 7:
                return "defense"

# engine = Main()
# engine.run("potion.png", "trade.png")
#
# # Display the pictured
# # if top_left:
# #     cv2.rectangle(img, top_left, bottom_right, 250, 2)
# # cv2.imshow("OpenCV/Numpy normal", img)
#
# # Display the picture in grayscale
# # cv2.imshow('OpenCV/Numpy grayscale',
# #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))
#
# f = []
# for (dirpath, dirnames, filenames) in walk("trade_potions"):
#     f.extend(filenames)
#     break
# for file in f:
#     output = engine.scan("trade_potions/{}".format(file))
#     print("Trade in --> {}".format(output))