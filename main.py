from time import sleep
import pyautogui
import mss
import cv2
import PIL
import PIL.ImageGrab
import mss.tools
import time
import numpy
from random import choice
from random import randint
print("Starting bot...d")
sleep(5)
with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 200, "left": 560, "width": 598, "height": 480}

    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))

        # Display the picture
        cv2.imshow("OpenCV/Numpy normal", img)

        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        # Press "q" to quit

        stop = False
        x = 0
        y = 0
        for i in range(598):
            # This loop is scanning all the pixels for other colors than dark
            # Since the godlands in which this will be run is completely dark
            # If this program detects any kind of color it will automaticly move
            if i < 480:
                if i > 240 and i < 340:
                    continue
                else:
                    x = 0
                    for pixel in img[i, i]:
                        x += 1
                        if x == 2:
                            break
                        if pixel > 160:
                            print("{}.Move".format(i))
                            x = i
                            y = i
                            stop = True
            else:
                x = 0
                for pixel in img[479, i]:
                    x += 1
                    if x == 2:
                        break
                    if pixel > 120:
                        print("{}.Move".format(i))
                        y = 479
                        x = i
                        stop = True
            if stop:
                if y > 250:
                    pyautogui.keyDown("s")
                if y < 250:
                    pyautogui.keyDown("w")
                if x < 250:
                    pyautogui.keyDown("d")
                if x > 250:
                    pyautogui.keyDown("a")
                pyautogui.keyUp('a')
                pyautogui.keyUp('w')
                pyautogui.keyUp('s')
                pyautogui.keyUp('d')
                break
        if not stop:
            if randint(0, 400) > 200:
                pyautogui.keyDown("s")
            if randint(0, 400) < 200:
                pyautogui.keyDown("w")
            if randint(0, 400) < 200:
                pyautogui.keyDown("d")
            if randint(0, 400) > 200:
                pyautogui.keyDown("a")
            pyautogui.keyUp('a')
            pyautogui.keyUp('w')
            pyautogui.keyUp('s')
            pyautogui.keyUp('d')


        if cv2.waitKey(25) & 0xFF == ord("q"):
            # for i in range(6):
            #     for x in range(5):
            #         for y in range(len(img[i][x]) -1):
            #             print()
            #             rgb = PIL.ImageGrab.grab().load()[int(img[i][x][y]), int(img[i][x][y + 1])]
            #             if rgb[0] > 100 or rgb[1] > 100 or rgb[2] > 100:
            #                 print("Attack")
            cv2.destroyAllWindows()
            break