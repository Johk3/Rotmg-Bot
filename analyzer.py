from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2
from random import randint

class ColorLabeler:
    def __init__(self):
        # initialize the colors dictionary, containing the color
        # name as the key and the RGB tuple as the value
        colors = OrderedDict({
            "vitality": (253, 5, 42),
            "speed": (9, 142, 61),
            "defense": (16,15,14),
            "attack": (159, 14, 165),
            "vitdex": (198, 0, 23),
            "wisdom": (50, 85, 213),
            "mana": (231, 200, 85),
            "life": (96, 215, 226)})

        # allocate memory for the L*a*b* image, then initialize
        # the color names list
        self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
        self.colorNames = []

        # loop over the colors dictionary
        for (i, (name, rgb)) in enumerate(colors.items()):
            # update the L*a*b* array and the color names list
            self.lab[i] = rgb
            self.colorNames.append(name)

        # convert the L*a*b* array from the RGB color space
        # to L*a*b*
        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

    def label(self, image, c):
        # construct a mask for the contour, then compute the
        # average L*a*b* value for the masked region
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)
        mean = cv2.mean(image, mask=mask)[:3]

        # initialize the minimum distance found thus far
        minDist = (np.inf, None)

        # loop over the known L*a*b* color values
        for (i, row) in enumerate(self.lab):
            # compute the distance between the current L*a*b*
            # color value and the mean of the image
            d = dist.euclidean(row[0], mean)

            # if the distance is smaller than the current distance,
            # then update the bookkeeping variable
            # This is to detect dexterity
            if int(d) == 64:
                return "life"

            if int(d) == 112:
                return "mana"

            if int(d) == 119 or int(d) == 53:
                return "speed"

            if int(d) == 106 or int(d) == 107:
                return None

            if d < minDist[0]:
                minDist = (d, i)

        # return the name of the color with the smallest distance
        return self.colorNames[minDist[1]]


# # construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image",
#                 help="path to the input image",
#                 default="compare.png")
# args = vars(ap.parse_args())
#
# # load the image and resize it to a smaller factor so that
# # the shapes can be approximated better
# image = cv2.imread(args["image"])
# resized = imutils.resize(image, width=300)
# ratio = image.shape[0] / float(resized.shape[0])
#
# # blur the resized image slightly, then convert it to both
# # grayscale and the L*a*b* color spaces
# blurred = cv2.GaussianBlur(resized, (5, 5), 0)
# gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
# lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
# thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
#
# # find contours in the thresholded image
# cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
#                         cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if imutils.is_cv2() else cnts[1]
#
# # initialize the shape detector and color labeler
# cl = ColorLabeler()
# i = 0
# for c in cnts:
#     # compute the center of the contour
#     if i >= 1 and i <= 8:
#         M = cv2.moments(c)
#         cX = int((M["m10"] / M["m00"]) * ratio)
#         cY = int((M["m01"] / M["m00"]) * ratio)
#
#         # detect the shape of the contour and label the color
#         color = cl.label(lab, c)
#
#         # multiply the contour (x, y)-coordinates by the resize ratio,
#         # then draw the contours and the name of the shape and labeled
#         # color on the image
#         c = c.astype("float")
#         c *= ratio
#         c = c.astype("int")
#         text = "{}".format(color)
#         cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
#         cv2.putText(image, text, (cX - 15, cY - 5),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
#
#         # show the output image
#         cv2.imshow("Image", image)
#         cv2.waitKey(0)
#     i+=1


# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
#
# img = cv2.imread('compare.png',0)
# img2 = img.copy()
# template = cv2.imread('potions/defense.png',0)
# w, h = template.shape[::-1]
#
# # All the 6 methods for comparison in a list
# methods = 'cv2.TM_SQDIFF_NORMED'
#
# img = img2.copy()
# method = eval(methods)
#
# # Apply template Matching
# res = cv2.matchTemplate(img,template,method)
# print(res[0])
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#
# #print("MIN {}\nMAX {}\nMIN LOC {}\nMAX LOC {}".format(min_val, max_val, min_loc, max_loc))
#
# # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
# if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
#     top_left = min_loc
# else:
#     top_left = max_loc
# bottom_right = (top_left[0] + w, top_left[1] + h)
#
# cv2.rectangle(img,top_left, bottom_right, 255, 2)
#
# plt.subplot(121),plt.imshow(res)
# plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(img)
# plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
# plt.suptitle(methods)
#
# plt.show()