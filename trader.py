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

def doublecheck():
    tradein_potions = []
    while 1:
        sleep(2)
        with mss.mss() as sct:
            monitor = {"top": 520, "left": 1170, "width": 180, "height": 135}
            img = sct.grab(monitor)
            mss.tools.to_png(img.rgb, img.size, output="lab/realtrade.png")
            engine = Main()
            engine.run("lab/potion.png", "lab/realtrade.png")
            f = []
            for (dirpath, dirnames, filenames) in walk("lab/trade_potions"):
                f.extend(filenames)
                break
            if f:
                for file in f:
                    output = engine.scan("lab/trade_potions/{}".format(file))
                    print("Trade in --> {}".format(output))
                    tradein_potions.append(output)
            if output:
                return tradein_potions

def accept():
    with mss.mss() as sct:
        monitor = {"top": 480, "left": 1160, "width": 100, "height": 40}
        img = sct.grab(monitor)
        mss.tools.to_png(img.rgb, img.size, output="tradeconfirmation.png")
        im = Image.open("tradeconfirmation.png")
        pix = im.load()
        for i in range(im.size[0]):
            if i >= 39:
                color = pix[i, 39]
                if color[0] == 113 and color[1] == 139 and color[2] == 80:
                    return True
            else:
                color = pix[i, i]
                if color[0] == 113 and color[1] == 139 and color[2] == 80:
                    return True
        return False

def find_trade(file):
    img = Image.open(file)
    colors = img.getcolors(256) #put a higher value if there are many colors in your image
    max_occurence, most_present = 0, 0
    check = 0
    try:
        for c in colors:
            if c[0] > max_occurence:
                (max_occurence, most_present) = c
        for value in most_present:
            if value == 255:
                check += 1
        if check == 3:
            print("Processing Trade...")
            return True
        return False
    except TypeError:
        return None

def analyzetrade():
    tradein_potions = []
    check = True
    output = None
    with mss.mss() as sct:
        monitor = {"top": 662, "left": 1272, "width": 70, "height": 34}
        img = sct.grab(monitor)
        mss.tools.to_png(img.rgb, img.size, output="trade.png")
        color = find_trade("trade.png")
        # color = True
    if color:
        mousex = 1312
        mouseY = 685
        offsetX = 13
        offsetY = 10
        pyautogui.moveTo(mouseX, mouseY)
        pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
        pyautogui.click(1325, 675)
        y = 0
        while y < 7:
            sleep(3)
            with mss.mss() as sct:
                monitor = {"top": 520, "left": 1170, "width": 180, "height": 135}
                img = sct.grab(monitor)
                mss.tools.to_png(img.rgb, img.size, output="lab/realtrade.png")
                engine = Main()
                engine.run("lab/potion.png", "lab/realtrade.png")
                f = []
                for (dirpath, dirnames, filenames) in walk("lab/trade_potions"):
                    f.extend(filenames)
                    break
                if f:
                    for file in f:
                        output = engine.scan("lab/trade_potions/{}".format(file))
                        print("Trade in --> {}".format(output))
                        tradein_potions.append(output)
                if output:
                    return tradein_potions
                    check = False
                y += 1


def selectpotion(potions, potionz):
    mouseX = 1161
    mouseY = 460
    weight = 100
    try:
        potion = potions[potionz]
        tradeX = mouseX + potion[0]
        tradeY = mouseY + potion[1]
        pyautogui.moveTo(tradeX, tradeY, 1)
        pyautogui.moveTo(tradeX, tradeY - weight, 1)
        pyautogui.click(tradeX, tradeY - weight)
        return True
    except Exception as e:
        return False


def analyzeimage():
    with mss.mss() as sct:
        monitor = {"top": 460, "left": 1160, "width": 197, "height": 114}
        found_potions = {}

        # Display the pictured
        # if top_left:
        #     cv2.rectangle(img, top_left, bottom_right, 250, 2)
        # cv2.imshow("OpenCV/Numpy normal", img)

        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        sct_image = sct.grab(monitor)
        mss.tools.to_png(sct_image.rgb, sct_image.size, output="compare.png")

        imgpath = "compare.png"

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
                color = cl.label(lab, c)

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
                    found_potions[color] = [cX, cY]
            i += 1
        return found_potions


if __name__ == "__main__":
    with mss.mss() as sct:
        # Part of the screen to capture
        with open("username.txt", "r") as txt:
            username = txt.read()
        mouseX = 1161
        mouseY = 460
        print("Press Q until I stop!\nBot started...")
        sleep(5)
        quit = True
        potion_results = analyzeimage()
        potions = ["attack", "vitdex", "defense", "mana", "speed", "wisdom"]
        while quit:
            folder = 'lab/trade_potions'
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    # elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception:
                    pass
            try:
                if keyboard.is_pressed('q'):
                    quit = False
                    print("Quitting...")
            except Exception:
                pass
            # pyautogui.moveTo(mouseX, mouseY)
            monitor = {"top": 460, "left": 1160, "width": 197, "height": 114}
            word = ""
            try:
                potion_results["life"]
                word = "LIFE"
            except Exception:
                pass
            try:
                potion_results["defense"]
                word = "DEFENSE"
            except Exception:
                pass
            try:
                potion_results["attack"]
                word = "ATTACK"
            except Exception:
                pass
            pyautogui.press("enter")
            sleep(0.2)
            pyautogui.typewrite("SELLING {}: {} SELLING {}: {} SELLING {}: {} SELLING {}: {} SELLING {}: {} SELLING {}:"
                                " {} SELLING {}: {} SELLING "
                                "{}: {}".format(word, username, word, username, word, username, word, username, word, username, word, username, word, username, word, username))
            pyautogui.press("enter")
            # potion = potion_results[potions[0]]
            # try:
            #     value = randint(1, len(potions)-1)
            #     topotion = potion_results[potions[value]]
            #     pyautogui.moveTo(mouseX + potion[0], mouseY + potion[1])
            #     pyautogui.dragTo(mouseX + topotion[0], mouseY + topotion[1], 0.5)
            # except Exception:
            #     print("Not fount {}".format(potions[value]))
            # exit(0)
            tradein = analyzetrade()
            if tradein:
                cnt = Counter()
                cntcheck = Counter()
                weight = 100
                print("Trading...")
                print(len(tradein))
                for potion in tradein:
                    cnt[potion] += 1

                if len(tradein) >= 3 and not cnt["life"] and not cnt["mana"] and not cnt["defense"] and not cnt["attack"]:
                    option1 = selectpotion(potion_results, "defense")
                    if not option1:
                        option2 = selectpotion(potion_results, "attack")
                    if option2 or option1:
                        sleep(1)
                        tradecheck = doublecheck()
                        print("Confirming...")
                        for potion in tradecheck:
                            cntcheck[potion] += 1
                        if len(tradecheck) >= 3 and not cnt["life"] and not cnt["mana"] and not cnt["defense"] and not cnt["attack"]:
                            x = 0
                            while x != 10:
                                sleep(2)
                                confirmation = accept()
                                if confirmation:
                                    print("Confirmed")
                                    mousex = 1312
                                    mouseY = 685
                                    offsetX = 13
                                    offsetY = 10
                                    pyautogui.moveTo(mouseX, mouseY)
                                    pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                                    pyautogui.click(1325, 675)
                                    sleep(3)
                                    pyautogui.moveTo(mouseX, mouseY)
                                    pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                                    pyautogui.click(1325, 675)
                                    x = 9
                                x += 1

                if cnt["life"] == 1:
                    selectpotion(potion_results, "vitdex")
                    selectpotion(potion_results, "speed")
                    selectpotion(potion_results, "wisdom")
                    selectpotion(potion_results, "defense")
                    sleep(1)

                    tradecheck = doublecheck()
                    print("Confirming...")
                    for potion in tradecheck:
                        cntcheck[potion] += 1
                    if cntcheck["life"] == 1:
                        x = 0
                        while x != 10:
                            sleep(2)
                            confirmation = accept()
                            if confirmation:
                                print("Confirmed")
                                mousex = 1312
                                mouseY = 685
                                offsetX = 13
                                offsetY = 10
                                pyautogui.moveTo(mouseX, mouseY)
                                pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                                pyautogui.click(1325, 675)
                                sleep(3)
                                tradecheck = doublecheck()
                                print("Confirming...")
                                for potion in tradecheck:
                                    cntcheck[potion] += 1
                                if cntcheck["life"] == 1:
                                    pyautogui.moveTo(mouseX, mouseY)
                                    pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                                    pyautogui.click(1325, 675)
                                x = 9
                            x += 1

                if cnt["defense"] == 1 and len(tradein) == 1:
                    selectpotion(potion_results, "speed")
                    selectpotion(potion_results, "wisdom")
                    selectpotion(potion_results, "vitdex")

                    tradecheck = doublecheck()
                    print("Confirming...")
                    for potion in tradecheck:
                        cntcheck[potion] += 1
                    if cntcheck["defense"] == 1 and len(tradecheck) == 1:
                        x = 0
                        while x != 10:
                            sleep(2)
                            confirmation = accept()
                            if confirmation:
                                print("Confirmed")
                                mousex = 1312
                                mouseY = 685
                                offsetX = 13
                                offsetY = 10
                                pyautogui.moveTo(mouseX, mouseY)
                                pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                                pyautogui.click(1325, 675)
                                sleep(3)
                                pyautogui.moveTo(mouseX, mouseY)
                                pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                                pyautogui.click(1325, 675)
                                x = 9
                            x += 1
                if cnt["defense"] == 7 or cnt["defense"] >= 3 and cnt["attack"] >= 4:
                    selectpotion(potion_results, "life")

                    tradecheck = doublecheck()
                    print("Confirming...")
                    for potion in tradecheck:
                        cntcheck[potion] += 1
                    if cntcheck["defense"] == 1 and len(tradecheck) == 1:
                        x = 0
                        while x != 10:
                            sleep(2)
                            confirmation = accept()
                            if confirmation:
                                print("Confirmed")
                                mousex = 1312
                                mouseY = 685
                                offsetX = 13
                                offsetY = 10
                                pyautogui.moveTo(mouseX, mouseY)
                                pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                                pyautogui.click(1325, 675)
                                sleep(3)
                                pyautogui.moveTo(mouseX, mouseY)
                                pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                                pyautogui.click(1325, 675)
                                x = 9
                            x += 1



