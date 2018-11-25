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

pyautogui.FAILSAFE = False

def tovault(potions, chosenpotion):
    mousex = 1312
    mouseY = 685
    offsetX = 50
    offsetY = 10
    mouseX = 1161

    sleep(2)
    pyautogui.keyDown('w')
    sleep(2)
    pyautogui.keyUp('w')
    quit = False
    while not quit:
        with mss.mss() as sct:
            pyautogui.keyDown('d')
            sleep(0.01)
            pyautogui.keyUp('d')
            monitor = {"top": 662, "left": 1232, "width": 70, "height": 34}
            img = sct.grab(monitor)
            mss.tools.to_png(img.rgb, img.size, output="vault.png")
            file = "vault.png"
            img = Image.open(file)
            colors = img.getcolors(256)
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
                    quit = True
            except TypeError:
                pass

    pyautogui.moveTo(mouseX, mouseY)
    pyautogui.moveTo(mousex - offsetX, mouseY - offsetY, 1)
    pyautogui.click(1325 - offsetX, 675)
    sleep(8)
    pyautogui.keyDown('w')
    sleep(0.2)
    pyautogui.keyUp('w')

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
            i += 1

        potionzee = chosenpotion
        for potionz, value in potionzee.items():
            print(potionz, value)
            mouseX = 1161
            mouseY = 460
            weight = 100
            loopty = value[0]
            if loopty > len(found_spots["empty"]) +1:
                loopamount = loopty
            else:
                loopamount = len(found_spots["empty"]) +1
            try:
                potionion = potions[potionz]
                i = 0
                for potion in potionion:
                    if i == loopamount:
                        return True
                    tradeX = mouseX + potion[0]
                    tradeY = mouseY + potion[1]
                    pyautogui.moveTo(tradeX, tradeY)
                    pyautogui.dragTo(mouseX - found_spots["empty"][i][0], mouseY - found_spots["empty"][i][1], 2)
                    i += 1
            except Exception as e:
                print(e)
                return False




def doublecheck():
    tradein_potions = []
    output = None
    x = 0
    while x < 8:
        sleep(2)
        folder = 'lab/trade_potions'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception:
                pass
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
            x += 1

def transaction(potion_results, cnt, cntpotion, cntis, potion, potionlooptime, multiplepotions = None, multiplecntpotions = None):
    cntcheck = Counter()
    mousex = 1312
    mouseY = 685
    offsetX = 13
    offsetY = 10


    if cntis <= cnt[cntpotion] <= cntis + 1:
        option1 = selectpotion(potion_results, potion, potionlooptime)
        xcheck = False

        if multiplepotions and not option1:
            for key, value in multiplepotions.items():
                selectpotion(potion_results, key, value[0])
                xcheck = True

        if not option1 and not xcheck:
            if potion_results["speed"] >= 2:
                selectpotion(potion_results, "speed", 2)
                xcheck = True
            elif potion_results["wisdom"] >= 2 and not xcheck:
                selectpotion(potion_results, "wisdom", 2)
                xcheck = True
            elif potion_results["vitdex"] >= 2 and not xcheck:
                selectpotion(potion_results, "vitdex", 2)
                xcheck = True
            elif not xcheck:
                selectpotion(potion_results, "vitdex", 1)
                selectpotion(potion_results, "wisdom", 1)
                selectpotion(potion_results, "speed", 1)

        sleep(4)
        if xcheck or option1:
            tradecheck = doublecheck()
            print("Confirming...")
            cntcheck = Counter()
            for potion in tradecheck:
                cntcheck[potion] += 1
            if cntis <= cntcheck[cntpotion] <= cntis + 1:
                x = 0
                while x != 10:
                    sleep(2)
                    confirmation = accept()
                    if confirmation:
                        print("Confirmed")
                        sleep(1)
                        tradecheck = doublecheck()
                        print("Doublechecking...")
                        cntcheck = Counter()
                        for potion in tradecheck:
                            cntcheck[potion] += 1
                        if cntis <= cntcheck[cntpotion] <= cntis + 1:
                            pyautogui.moveTo(mouseX, mouseY)
                            pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 0.2)
                            pyautogui.click(1325, 675)
                            return True
                        else:
                            pyautogui.moveTo(mouseX, mouseY)
                            pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                            pyautogui.click(1325 - 100, 675)
                            return False
                    x = 9
                x += 1
        else:
            pyautogui.moveTo(mouseX, mouseY)
            pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
            pyautogui.click(1325 - 100, 675)
            return False

    if multiplecntpotions:
        for key, value in multiplecntpotions.items():
            cntpotion = key
            cntis = value[0]
            if cntis <= cnt[cntpotion] <= cntis + 1:
                option1 = selectpotion(potion_results, potion, potionlooptime)
                xcheck = False

                if multiplepotions and not option1:
                    for key, value in multiplepotions.items():
                        selectpotion(potion_results, key, value[0])
                        print(key, value[0])
                        xcheck = True

                if not option1 and not xcheck:
                    if potion_results["speed"] >= 2:
                        selectpotion(potion_results, "speed", 2)
                        xcheck = True
                    elif potion_results["wisdom"] >= 2 and not xcheck:
                        selectpotion(potion_results, "wisdom", 2)
                        xcheck = True
                    elif potion_results["vitdex"] >= 2 and not xcheck:
                        selectpotion(potion_results, "vitdex", 2)
                        xcheck = True
                    elif not xcheck:
                        selectpotion(potion_results, "vitdex", 1)
                        selectpotion(potion_results, "wisdom", 1)
                        selectpotion(potion_results, "speed", 1)

                sleep(4)
                cntcheck = Counter()
                if xcheck or option1:
                    tradecheck = doublecheck()
                    print("Confirming...")
                    for potion in tradecheck:
                        cntcheck[potion] += 1
                    if cntis <= cntcheck[cntpotion] <= cntis + 1:
                        x = 0
                        while x != 10:
                            sleep(2)
                            confirmation = accept()
                            if confirmation:
                                print("Confirmed")
                                sleep(1)
                                tradecheck = doublecheck()
                                print("Doublechecking...")
                                cntcheck = Counter()
                                for potion in tradecheck:
                                    cntcheck[potion] += 1
                                if cntis <= cntcheck[cntpotion] <= cntis + 1:
                                    pyautogui.moveTo(mouseX, mouseY)
                                    pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 0.2)
                                    pyautogui.click(1325, 675)
                                    return True
                                else:
                                    pyautogui.moveTo(mouseX, mouseY)
                                    pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                                    pyautogui.click(1325 - 100, 675)
                                    return False
                            x = 9
                        x += 1
            else:
                pass

    else:
        return False

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
        while y < 5:
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


def selectpotion(potions, potionz, loopamount=8):
    mouseX = 1161
    mouseY = 460
    weight = 100
    try:
        potionion = potions[potionz]
        i = 0
        for potion in potionion:
            if i == loopamount:
                return True
            tradeX = mouseX + potion[0]
            tradeY = mouseY + potion[1]
            pyautogui.moveTo(tradeX, tradeY, 0.2)
            pyautogui.moveTo(tradeX, tradeY - weight, 0.2)
            pyautogui.click(tradeX, tradeY - weight)
            i += 1
        if i >= 1:
            return True
    except Exception as e:
        return False


def analyzeimage():
    with mss.mss() as sct:
        monitor = {"top": 460, "left": 1160, "width": 197, "height": 114}
        found_potions = defaultdict(list)

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
                    found_potions[color].append([cX, cY])
            i += 1
        return found_potions


if __name__ == "__main__":
    print("Starting...")
    sleep(3)
    pyautogui.keyDown('s')
    sleep(8)
    pyautogui.keyUp('s')
    with mss.mss() as sct:
        # Part of the screen to capture
        with open("username.txt", "r") as txt:
            username = txt.read()
        extracheck = True
        word = ""
        buy = ""
        mouseX = 1161
        mouseY = 460
        print("Press Q until I stop!\nBot started...")
        quit = True
        potion_results = analyzeimage()
        potions = ["attack", "vitdex", "defense", "mana", "speed", "wisdom"]

        potionzee = defaultdict(list)
        potionzee["defense"].append(2)
        potionzee["wisdom"].append(1)
        potionzee["speed"].append(1)
        potionzee["vitdex"].append(1)

        tovault(potion_results, potionzee)
        exit(0)
        while quit:
            if not extracheck:
                sleep(2)
                potion_results = analyzeimage()
                extracheck = True
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
            if extracheck:
                word = ""
                buy = ""
                sellcheck = False
                if potion_results["life"]:
                    word = "LIFE"
                    buy = "6 DEFENSE"
                    sellcheck = True
                if potion_results["defense"]:
                    if not sellcheck and len(potion_results["defense"]) >= 4:
                        word = "DEFENSE"
                        buy = "LIFE"
                        sellcheck = True
                    if not sellcheck and len(potion_results["defense"]) >= 2:
                        word = "DEFENSE"
                        buy = "MANA"
                        sellcheck = True
                if potion_results["mana"]:
                    if not sellcheck:
                        word = "MANA"
                        buy = "3 DEFENSE"
                        sellcheck = True
                if potion_results["attack"]:
                    if not sellcheck:
                        potion_results["attack"]
                        word = "ATTACK"
                        buy = "DEFENSE"
                        sellcheck = True
                if potion_results["speed"] or potion_results["vitdex"]:
                    if not sellcheck:
                        potion_results["speed"]
                        word = "SPEED"
                        buy = "DEFENSE"
                        sellcheck = True
            if len(potion_results["defense"]) >= 5:
                word = "DEFENSE"
                buy = "LIFE"
            if len(potion_results["attack"]) >= 5:
                word = "ATTACK"
                buy = "LIFE"
            if len(potion_results)/2 >= 4:
                if potion_results["mana"]:
                    word = "MANA"
                    buy = "3 DEF"
            pyautogui.press("enter")
            sleep(0.2)
            pyautogui.typewrite("  [S] {} TRADE: {} [B] > {}   [S] > {} TRADE: {} [B] > {}".format(word, username, buy, word, username, buy))
            pyautogui.press("enter")
            potion = potion_results[potions[0]]
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

                mousex = 1312
                mouseY = 685
                offsetX = 13
                offsetY = 10
                outputcheck = False

                # This is where you can add your own rules
                # if you uncomment the line of code that is below this text you can make some rules for the bot
                # So the first line where it says potion_results["attack"], it means that if you have attack in your
                # Inventory do this:
                # Then it does a transaction, I will tell you what all the arguments do in the transaction(arguments)
                # The first argument is potion_results, you dont need to know what that does, it just needs to be there
                # The next argument is cnt which is also another thing that needs to be there
                # The next is "defense" which means that if the other people has defense in their inventory
                # The next is 1 which means how many defenses are being traded
                # So if 1 defense is being traded by the other party then do this
                # The next is "attack" which is what your character will choose to trade
                # The next is 1, so the bot trades 1 attack for 1 defense

                # if potion_results["attack"]:
                #     output = transaction(potion_results, cnt, "defense", 1, "attack", 1)
                # if output:
                #     outputcheck = True
                #     print("Successful Transaction")

                # ------------------------

                # if not outputcheck:
                #     if potion_results["attack"]:
                #         output = transaction(potion_results, cnt, "defense", 1, "attack", 1)
                #
                #     if output:
                #         outputcheck = True
                #         print("Successful Transaction")

                # ------------------------

                # if not outputcheck:
                #     if potion_results["attack"]:
                #         output = transaction(potion_results, cnt, "defense", 1, "attack", 1)
                #
                #     if output:
                #         outputcheck = True
                #         print("Successful Transaction")

                # ------------------------
                # From here on, dont change anything!

                output = False

                if not outputcheck and not cnt["life"] and not cnt["defense"] and not cnt["attack"] and not cnt["mana"]:
                    if cnt["speed"] or cnt["wisdom"] or cnt["vitdex"]:
                        multiplecntoptions = defaultdict(list)
                        multiplecntoptions["vitdex"].append(3)
                        multiplecntoptions["wisdom"].append(3)
                        if potion_results["attack"]:
                            output = transaction(potion_results, cnt, "speed", 3, "attack", 1)
                        if potion_results["defense"]:
                            output = transaction(potion_results, cnt, "speed", 3, "defense", 1)

                    if output:
                        outputcheck = True
                        print("Successful Transaction")

                if not outputcheck:
                    if cnt["attack"] >= 3:
                        output = transaction(potion_results, cnt, "attack", 3, "mana", 1)
                    if cnt["defense"] >= 3:
                        output = transaction(potion_results, cnt, "defense", 3, "mana", 1)

                    if output:
                        outputcheck = True
                        print("Successful Transaction")

                if not outputcheck and cnt["life"] == 1:
                    if len(potion_results["attack"]) >= 5:
                        output = transaction(potion_results, cnt, "life", 1, "attack", 5)
                    if len(potion_results["defense"]) >= 3:
                        output = transaction(potion_results, cnt, "life", 1, "defense", 5)

                    if output:
                        outputcheck = True
                        print("Successful Transaction")

                if not outputcheck and cnt["mana"]:
                    if len(potion_results["attack"]) >= 2:
                        output = transaction(potion_results, cnt, "mana", 1, "attack", 2)
                    if len(potion_results["defense"]) >= 2:
                        output = transaction(potion_results, cnt, "mana", 1, "defense", 2)

                    if output:
                        outputcheck = True
                        print("Successful Transaction")

                if not outputcheck and cnt["life"] and len(tradein) >= 3:
                    if len(potion_results["attack"]) >= 5:
                        output = transaction(potion_results, cnt, "life", 1, "attack", 5)
                    if len(potion_results["defense"]) >= 3:
                        output = transaction(potion_results, cnt, "life", 1, "defense", 5)

                    if output:
                        outputcheck = True
                        print("Successful Transaction")

                if not outputcheck and cnt["mana"] and len(tradein) >= 3:
                    if len(potion_results["attack"]) >= 3:
                        output = transaction(potion_results, cnt, "mana", 1, "attack", 3)
                    if len(potion_results["defense"]) >= 3:
                        output = transaction(potion_results, cnt, "mana", 1, "defense", 3)

                    if output:
                        outputcheck = True
                        print("Successful Transaction")

                if not outputcheck and cnt["life"]:
                    if len(potion_results["attack"]) >= 5:
                        output = transaction(potion_results, cnt, "life", 1, "attack", 5)
                    if len(potion_results["defense"]) >= 5:
                        output = transaction(potion_results, cnt, "life", 1, "defense", 5)
                    if len(potion_results["mana"] >= 2):
                        output = transaction(potion_results, cnt, "life", 1, "mana", 3)

                    if output:
                        outputcheck = True
                        print("Successful Transaction")

                if not outputcheck:
                    if potion_results["mana"]:
                        output = transaction(potion_results, cnt, "mana", 1, "defense", 2)

                    if output:
                        outputcheck = True
                        print("Successful Transaction")

                if not outputcheck:
                    if potion_results["attack"]:
                        output = transaction(potion_results, cnt, "defense", 1, "attack", 1)

                    if output:
                        outputcheck = True
                        print("Successful Transaction")

                if not outputcheck:
                    multiplepotions = defaultdict(list)
                    multiplepotions["mana"].append(1)
                    multiplepotions["attack"].append(5)
                    output = transaction(potion_results, cnt, "life", 1, "defense", 5, multiplepotions)
                    if output:
                        print("Successful Transaction")
                        outputcheck = True

                if not outputcheck:
                    multiplepotions = defaultdict(list)
                    multiplepotions["attack"].append(1)
                    multiplecntoptions = defaultdict(list)
                    multiplecntoptions["vitdex"].append(3)
                    multiplecntoptions["wisdom"].append(3)
                    output = transaction(potion_results, cnt, "speed", 3, "defense", 1, multiplepotions, multiplecntoptions)
                    if output:
                        print("Successful Transaction")
                        outputcheck = True

                if not outputcheck and potion_results["life"]:
                    output = transaction(potion_results, cnt, "mana", 4, "life", 1)
                    if output:
                        print("Successful Transaction")
                        outputcheck = True


                if not outputcheck and potion_results["life"]:
                    if cnt["attack"] >= 5 and len(tradein) >= 6:
                        output = transaction(potion_results, cnt, "attack", 5, "life", 1)
                    else:
                        output = transaction(potion_results, cnt, "attack", 5, "life", 1)
                    if output:
                        print("Successful Transaction")
                        outputcheck = True

                if not outputcheck and potion_results["life"]:
                    if cnt["defense"] >= 5 and len(tradein) >= 6:
                        output = transaction(potion_results, cnt, "defense", 5, "life", 1)
                    else:
                        output = transaction(potion_results, cnt, "defense", 5, "life", 1)
                    if output:
                        print("Successful Transaction")
                        outputcheck = True

                if outputcheck:
                    extracheck = False

                # if cnt["defense"] >= 6 or cnt["attack"] >= 6:
                #     selectpotion(potion_results, "life", 1)
                #     sleep(4)
                #     tradecheck = doublecheck()
                #     print("Confirming...")
                #     for potion in tradecheck:
                #         cntcheck[potion] += 1
                #     if cntcheck["defense"] >= 6 or cntcheck["attack"] >= 6:
                #         x = 0
                #         while x != 10:
                #             sleep(2)
                #             confirmation = accept()
                #             if confirmation:
                #                 print("Confirmed")
                #                 mousex = 1312
                #                 mouseY = 685
                #                 offsetX = 13
                #                 offsetY = 10
                #                 pyautogui.moveTo(mouseX, mouseY)
                #                 pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                 pyautogui.click(1325, 675)
                #                 sleep(3)
                #                 tradecheck = doublecheck()
                #                 print("Doublechecking...")
                #                 cntcheck = Counter()
                #                 for potion in tradecheck:
                #                     cntcheck[potion] += 1
                #                 if cntcheck["defense"] >= 6 or cntcheck["attack"] >= 6:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                     pyautogui.click(1325, 675)
                #                 else:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #                     pyautogui.click(1325 - 100, 675)
                #             x = 9
                #         x += 1
                #     else:
                #         pyautogui.moveTo(mouseX, mouseY)
                #         pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #         pyautogui.click(1325 - 100, 675)
                #
                # if cnt["life"]:
                #     option1 = selectpotion(potion_results, "attack", 5)
                #     option2 = False
                #     xcheck = False
                #     if not option1:
                #         option2 = selectpotion(potion_results, "defense", 5)
                #     sleep(4)
                #     if xcheck or option1:
                #         tradecheck = doublecheck()
                #         print("Confirming...")
                #         for potion in tradecheck:
                #             cntcheck[potion] += 1
                #         if cntcheck["life"]:
                #             x = 0
                #             while x != 10:
                #                 sleep(2)
                #                 confirmation = accept()
                #                 if confirmation:
                #                     print("Confirmed")
                #                     mousex = 1312
                #                     mouseY = 685
                #                     offsetX = 13
                #                     offsetY = 10
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                     pyautogui.click(1325, 675)
                #                     sleep(3)
                #                     tradecheck = doublecheck()
                #                     print("Doublechecking...")
                #                     cntcheck = Counter()
                #                     for potion in tradecheck:
                #                         cntcheck[potion] += 1
                #                     if cntcheck["life"]:
                #                         pyautogui.moveTo(mouseX, mouseY)
                #                         pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                         pyautogui.click(1325, 675)
                #                     else:
                #                         pyautogui.moveTo(mouseX, mouseY)
                #                         pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #                         pyautogui.click(1325 - 100, 675)
                #                 x = 9
                #             x += 1
                #
                # if cnt["defense"] == 1:
                #     option1 = selectpotion(potion_results, "attack", 1)
                #     option2 = False
                #     xcheck = False
                #     if not option1:
                #         if potion_results["speed"] >= 2:
                #             selectpotion(potion_results, "speed", 2)
                #             xcheck = True
                #         elif potion_results["wisdom"] >= 2 and not xcheck:
                #             selectpotion(potion_results, "wisdom", 2)
                #             xcheck = True
                #         elif potion_results["vitdex"] >= 2 and not xcheck:
                #             selectpotion(potion_results, "vitdex", 2)
                #             xcheck = True
                #         elif not xcheck:
                #             selectpotion(potion_results, "vitdex", 1)
                #             selectpotion(potion_results, "wisdom", 1)
                #             selectpotion(potion_results, "speed", 1)
                #     sleep(4)
                #     if xcheck or option1:
                #         tradecheck = doublecheck()
                #         print("Confirming...")
                #         for potion in tradecheck:
                #             cntcheck[potion] += 1
                #         if cntcheck["defense"] == 1:
                #             x = 0
                #             while x != 10:
                #                 sleep(2)
                #                 confirmation = accept()
                #                 if confirmation:
                #                     print("Confirmed")
                #                     mousex = 1312
                #                     mouseY = 685
                #                     offsetX = 13
                #                     offsetY = 10
                #                     sleep(3)
                #                     tradecheck = doublecheck()
                #                     print("Doublechecking...")
                #                     cntcheck = Counter()
                #                     for potion in tradecheck:
                #                         cntcheck[potion] += 1
                #                     if cntcheck["defense"] == 1:
                #                         pyautogui.moveTo(mouseX, mouseY)
                #                         pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                         pyautogui.click(1325, 675)
                #                     else:
                #                         pyautogui.moveTo(mouseX, mouseY)
                #                         pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #                         pyautogui.click(1325 - 100, 675)
                #                 x = 9
                #             x += 1
                #     else:
                #         pyautogui.moveTo(mouseX, mouseY)
                #         pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #         pyautogui.click(1325 - 100, 675)
                #
                # if len(tradein) == 0:
                #     sleep(6)
                #     tradecheck = doublecheck()
                #     if tradecheck:
                #         pass
                #     else:
                #         offsetX = 13
                #         offsetY = 10
                #         pyautogui.moveTo(mouseX, mouseY)
                #         pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #         pyautogui.click(1325 - 100, 675)
                #
                # if len(tradein) >= 3:
                #     print("YUH")
                #     option1 = selectpotion(potion_results, "attack", 1)
                #     option2 = False
                #     if not option1:
                #         option2 = selectpotion(potion_results, "defense", 1)
                #     sleep(4)
                #     if option2 or option1:
                #         tradecheck = doublecheck()
                #         print("Confirming...")
                #         for potion in tradecheck:
                #             cntcheck[potion] += 1
                #         if len(tradecheck) >= 3:
                #             x = 0
                #             while x != 10:
                #                 sleep(2)
                #                 confirmation = accept()
                #                 if confirmation:
                #                     print("Confirmed")
                #                     mousex = 1312
                #                     mouseY = 685
                #                     offsetX = 13
                #                     offsetY = 10
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                     pyautogui.click(1325, 675)
                #                     sleep(3)
                #                     tradecheck = doublecheck()
                #                     print("Doublechecking...")
                #                     cntcheck = Counter()
                #                     for potion in tradecheck:
                #                         cntcheck[potion] += 1
                #                     if len(tradecheck) >= 3:
                #                         pyautogui.moveTo(mouseX, mouseY)
                #                         pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                         pyautogui.click(1325, 675)
                #                     else:
                #                         pyautogui.moveTo(mouseX, mouseY)
                #                         pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #                         pyautogui.click(1325 - 100, 675)
                #                 x = 9
                #             x += 1
                #     else:
                #         pyautogui.moveTo(mouseX, mouseY)
                #         pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #         pyautogui.click(1325 - 100, 675)
                #
                # if len(tradein) >= 3 and cnt["defense"] or cnt["attack"]:
                #     selectpotion(potion_results, "mana", 1)
                #     sleep(4)
                #
                #     tradecheck = doublecheck()
                #     print("Confirming...")
                #     for potion in tradecheck:
                #         cntcheck[potion] += 1
                #     if len(tradein) >= 3 and cntcheck["defense"] or cntcheck["attack"]:
                #         x = 0
                #         while x != 10:
                #             sleep(2)
                #             confirmation = accept()
                #             if confirmation:
                #                 print("Confirmed")
                #                 mousex = 1312
                #                 mouseY = 685
                #                 offsetX = 13
                #                 offsetY = 10
                #                 pyautogui.moveTo(mouseX, mouseY)
                #                 pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                 pyautogui.click(1325, 675)
                #                 sleep(3)
                #                 tradecheck = doublecheck()
                #                 print("Doublechecking...")
                #                 cntcheck = Counter()
                #                 for potion in tradecheck:
                #                     cntcheck[potion] += 1
                #                 if len(tradein) >= 3 and cntcheck["defense"] or cntcheck["attack"]:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                     pyautogui.click(1325, 675)
                #                 else:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #                     pyautogui.click(1325 - 100, 675)
                #             x = 9
                #         x += 1
                #     else:
                #         pyautogui.moveTo(mouseX, mouseY)
                #         pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #         pyautogui.click(1325 - 100, 675)
                #
                # if cnt["defense"] >= 4 and cnt["defense"] <= 5:
                #     selectpotion(potion_results, "mana", 1)
                #     sleep(4)
                #
                #     tradecheck = doublecheck()
                #     print("Confirming...")
                #     for potion in tradecheck:
                #         cntcheck[potion] += 1
                #     if cntcheck["defense"] >= 4 and cnt["defense"] < 6:
                #         x = 0
                #         while x != 10:
                #             sleep(2)
                #             confirmation = accept()
                #             if confirmation:
                #                 print("Confirmed")
                #                 mousex = 1312
                #                 mouseY = 685
                #                 offsetX = 13
                #                 offsetY = 10
                #                 pyautogui.moveTo(mouseX, mouseY)
                #                 pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                 pyautogui.click(1325, 675)
                #                 sleep(3)
                #                 tradecheck = doublecheck()
                #                 print("Doublechecking...")
                #                 cntcheck = Counter()
                #                 for potion in tradecheck:
                #                     cntcheck[potion] += 1
                #                 if cntcheck["defense"] >= 4 and cnt["defense"] < 6:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                     pyautogui.click(1325, 675)
                #                 else:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #                     pyautogui.click(1325 - 100, 675)
                #             x = 9
                #         x += 1
                #     else:
                #         pyautogui.moveTo(mouseX, mouseY)
                #         pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #         pyautogui.click(1325 - 100, 675)
                #
                # if cnt["speed"] >= 3 and potion_results["defense"]:
                #     selectpotion(potion_results, "defense", 1)
                #     sleep(4)
                #
                #     tradecheck = doublecheck()
                #     print("Confirming...")
                #     for potion in tradecheck:
                #         cntcheck[potion] += 1
                #     if cntcheck["speed"] >= 3 and potion_results["defense"]:
                #         x = 0
                #         while x != 10:
                #             sleep(2)
                #             confirmation = accept()
                #             if confirmation:
                #                 print("Confirmed")
                #                 mousex = 1312
                #                 mouseY = 685
                #                 offsetX = 13
                #                 offsetY = 10
                #                 pyautogui.moveTo(mouseX, mouseY)
                #                 pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                 pyautogui.click(1325, 675)
                #                 sleep(3)
                #                 tradecheck = doublecheck()
                #                 print("Doublechecking...")
                #                 cntcheck = Counter()
                #                 for potion in tradecheck:
                #                     cntcheck[potion] += 1
                #                 if cntcheck["speed"] >= 3 and potion_results["defense"]:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                     pyautogui.click(1325, 675)
                #                 else:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #                     pyautogui.click(1325 - 100, 675)
                #             x = 9
                #         x += 1
                #     else:
                #         pyautogui.moveTo(mouseX, mouseY)
                #         pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #         pyautogui.click(1325 - 100, 675)
                # if cnt["mana"] >= 3 and potion_results["life"]:
                #     selectpotion(potion_results, "life", 1)
                #     sleep(4)
                #
                #     tradecheck = doublecheck()
                #     print("Confirming...")
                #     for potion in tradecheck:
                #         cntcheck[potion] += 1
                #     if cntcheck["mana"] >= 3 and potion_results["life"]:
                #         x = 0
                #         while x != 10:
                #             sleep(2)
                #             confirmation = accept()
                #             if confirmation:
                #                 print("Confirmed")
                #                 mousex = 1312
                #                 mouseY = 685
                #                 offsetX = 13
                #                 offsetY = 10
                #                 tradecheck = doublecheck()
                #                 print("Doublechecking...")
                #                 cntcheck = Counter()
                #                 for potion in tradecheck:
                #                     cntcheck[potion] += 1
                #                 if cntcheck["mana"] >= 3 and potion_results["life"]:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                     pyautogui.click(1325, 675)
                #                 else:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #                     pyautogui.click(1325 - 100, 675)
                #             x = 9
                #         x += 1
                #     else:
                #         pyautogui.moveTo(mouseX, mouseY)
                #         pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #         pyautogui.click(1325 - 100, 675)
                #
                # if cnt["attack"] >= 3 and potion_results["defense"]:
                #     selectpotion(potion_results, "defense", 2)
                #     sleep(4)
                #
                #     tradecheck = doublecheck()
                #     print("Confirming...")
                #     for potion in tradecheck:
                #         cntcheck[potion] += 1
                #     if cntcheck["attack"] >= 3 and potion_results["defense"]:
                #         x = 0
                #         while x != 10:
                #             sleep(2)
                #             confirmation = accept()
                #             if confirmation:
                #                 print("Confirmed")
                #                 mousex = 1312
                #                 mouseY = 685
                #                 offsetX = 13
                #                 offsetY = 10
                #                 tradecheck = doublecheck()
                #                 print("Doublechecking...")
                #                 cntcheck = Counter()
                #                 for potion in tradecheck:
                #                     cntcheck[potion] += 1
                #                 if cntcheck["attack"] >= 3 and potion_results["defense"]:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                     pyautogui.click(1325, 675)
                #                 else:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #                     pyautogui.click(1325 - 100, 675)
                #             x = 9
                #         x += 1
                #     else:
                #         pyautogui.moveTo(mouseX, mouseY)
                #         pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #         pyautogui.click(1325 - 100, 675)
                #
                # mousex = 1312
                # mouseY = 685
                #
                # if cnt["defense"] == 1 and potion_results["attack"]:
                #     selectpotion(potion_results, "attack", 1)
                #     sleep(4)
                #
                #     tradecheck = doublecheck()
                #     print("Confirming...")
                #     for potion in tradecheck:
                #         cntcheck[potion] += 1
                #     if cntcheck["defense"] == 1 and potion_results["attack"]:
                #         x = 0
                #         while x != 10:
                #             sleep(2)
                #             confirmation = accept()
                #             if confirmation:
                #                 print("Confirmed")
                #                 mousex = 1312
                #                 mouseY = 685
                #                 offsetX = 13
                #                 offsetY = 10
                #                 tradecheck = doublecheck()
                #                 print("Doublechecking...")
                #                 cntcheck = Counter()
                #                 for potion in tradecheck:
                #                     cntcheck[potion] += 1
                #                 if cntcheck["defense"] == 1 and potion_results["attack"]:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                     pyautogui.click(1325, 675)
                #                 else:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #                     pyautogui.click(1325 - 100, 675)
                #             x = 9
                #         x += 1
                #     else:
                #         pyautogui.moveTo(mouseX, mouseY)
                #         pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #         pyautogui.click(1325 - 100, 675)
                #
                #
                # if cnt["mana"]:
                #     selectpotion(potion_results, "defense", 2)
                #     sleep(4)
                #
                #     tradecheck = doublecheck()
                #     print("Confirming...")
                #     for potion in tradecheck:
                #         cntcheck[potion] += 1
                #     if cntcheck["mana"]:
                #         x = 0
                #         while x != 10:
                #             sleep(2)
                #             confirmation = accept()
                #             if confirmation:
                #                 print("Confirmed")
                #                 mousex = 1312
                #                 mouseY = 685
                #                 offsetX = 13
                #                 offsetY = 10
                #                 tradecheck = doublecheck()
                #                 print("Doublechecking...")
                #                 cntcheck = Counter()
                #                 for potion in tradecheck:
                #                     cntcheck[potion] += 1
                #                 if cntcheck["mana"]:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                     pyautogui.click(1325, 675)
                #                 else:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #                     pyautogui.click(1325 - 100, 675)
                #             x = 9
                #         x += 1
                #     else:
                #         pyautogui.moveTo(mouseX, mouseY)
                #         pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #         pyautogui.click(1325 - 100, 675)
                #
                # if len(tradein) >= 3 and not cnt["life"] and not cnt["mana"] and not cnt["defense"] and not cnt["attack"]:
                #     option1 = selectpotion(potion_results, "defense", 1)
                #     option2 = False
                #     if not option1:
                #         option2 = selectpotion(potion_results, "attack", 1)
                #     if option2 or option1:
                #         sleep(4)
                #         tradecheck = doublecheck()
                #         print("Confirming...")
                #         for potion in tradecheck:
                #             cntcheck[potion] += 1
                #         if len(tradecheck) >= 3 and not cntcheck["life"] and not cntcheck["mana"] and not cntcheck["defense"] and not cntcheck["attack"]:
                #             x = 0
                #             while x < 10:
                #                 sleep(2)
                #                 confirmation = accept()
                #                 if confirmation:
                #                     print("Confirmed")
                #                     mousex = 1312
                #                     mouseY = 685
                #                     offsetX = 13
                #                     offsetY = 10
                #                     tradecheck = doublecheck()
                #                     print("Doublechecking...")
                #                     cntcheck = Counter()
                #                     for potion in tradecheck:
                #                         cntcheck[potion] += 1
                #                     print(cntcheck)
                #                     if len(tradecheck) >= 3 and not cntcheck["life"] and not cntcheck["mana"] and not cntcheck["defense"] and not cntcheck["attack"]:
                #                         pyautogui.moveTo(mouseX, mouseY)
                #                         pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                         pyautogui.click(1325, 675)
                #                     else:
                #                         pyautogui.moveTo(mouseX, mouseY)
                #                         pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #                         pyautogui.click(1325 - 100, 675)
                #                     x = 9
                #                 x += 1
                #         else:
                #             pyautogui.moveTo(mouseX, mouseY)
                #             pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #             pyautogui.click(1325 - 100, 675)
                #
                #
                # if len(tradein) >= 1:
                #     option1 = selectpotion(potion_results, "speed", 1)
                #     option2 = False
                #     if not option1:
                #         option2 = selectpotion(potion_results, "vitdex", 1)
                #     if option2 or option1:
                #         sleep(4)
                #         tradecheck = doublecheck()
                #         print("Confirming...")
                #         for potion in tradecheck:
                #             cntcheck[potion] += 1
                #         if cntcheck["defense"] == 6 or cntcheck["attack"] == 7:
                #             x = 0
                #             while x != 10:
                #                 sleep(2)
                #                 confirmation = accept()
                #                 if confirmation:
                #                     print("Confirmed")
                #                     mousex = 1312
                #                     mouseY = 685
                #                     offsetX = 13
                #                     offsetY = 10
                #                     tradecheck = doublecheck()
                #                     print("Doublechecking...")
                #                     cntcheck = Counter()
                #                     for potion in tradecheck:
                #                         cntcheck[potion] += 1
                #                     if cntcheck["defense"] == 6 or cntcheck["attack"] == 7:
                #                         pyautogui.moveTo(mouseX, mouseY)
                #                         pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                         pyautogui.click(1325, 675)
                #                     else:
                #                         pyautogui.moveTo(mouseX, mouseY)
                #                         pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #                         pyautogui.click(1325 - 100, 675)
                #                 x = 9
                #             x += 1
                #         else:
                #             pyautogui.moveTo(mouseX, mouseY)
                #             pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #             pyautogui.click(1325 - 100, 675)
                #
                # if cnt["speed"] >= 3 and potion_results["defense"]:
                #     selectpotion(potion_results, "defense", 1)
                #     sleep(4)
                #
                #     tradecheck = doublecheck()
                #     print("Confirming...")
                #     for potion in tradecheck:
                #         cntcheck[potion] += 1
                #     if cntcheck["speed"] >= 3 and potion_results["defense"]:
                #         x = 0
                #         while x != 10:
                #             sleep(2)
                #             confirmation = accept()
                #             if confirmation:
                #                 print("Confirmed")
                #                 mousex = 1312
                #                 mouseY = 685
                #                 offsetX = 13
                #                 offsetY = 10
                #                 pyautogui.moveTo(mouseX, mouseY)
                #                 pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                 pyautogui.click(1325, 675)
                #                 sleep(3)
                #                 tradecheck = doublecheck()
                #                 print("Doublechecking...")
                #                 cntcheck = Counter()
                #                 for potion in tradecheck:
                #                     cntcheck[potion] += 1
                #                 if cntcheck["speed"] >= 3 and potion_results["defense"]:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex + offsetX, mouseY - offsetY, 1)
                #                     pyautogui.click(1325, 675)
                #                 else:
                #                     pyautogui.moveTo(mouseX, mouseY)
                #                     pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #                     pyautogui.click(1325 - 100, 675)
                #             x = 9
                #         x += 1
                #     else:
                #         pyautogui.moveTo(mouseX, mouseY)
                #         pyautogui.moveTo(mousex - 100, mouseY - offsetY, 1)
                #         pyautogui.click(1325 - 100, 675)


