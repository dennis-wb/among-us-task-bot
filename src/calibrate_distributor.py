import cv2
import pyautogui
import numpy as np
import time

from task import Task


class CalibrateDistributor(Task):

    def is_current_task(self, screen):
        roi = screen[430:430 + 210, 780:780 + 270]

        ref = cv2.imread("../media/identifiers/calibrate_distributor_identifier.png")
        res = cv2.matchTemplate(roi, ref, cv2.TM_CCOEFF_NORMED)

        _, m, _, _ = cv2.minMaxLoc(res)
        return m > 0.9

    def do_task(self, screen):

        pyautogui.PAUSE = 0

        colors = ["yellow", "blue", "cyan"]
        offset = 266

        ref_rgb = [(255, 227, 0),  # yellow
                   (83, 98, 255),  # blue
                   (111, 249, 255)]  # cyan

        for i in range(3):
            aligned = False

            while not aligned:
                # Comparing pixel colors is sufficient here
                pix = pyautogui.pixel(1300, 232 + i * offset)

                epsilon = 10
                for j in range(3):
                    if abs(pix[j] - ref_rgb[i][j]) > epsilon:
                        break
                    aligned = True

                if aligned:
                    pyautogui.moveTo(1240, 310 + i * offset)
                    pyautogui.click()

        time.sleep(2)
