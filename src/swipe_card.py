import cv2
import numpy as np
import pyautogui
import time

from task import Task


class SwipeCard(Task):

    def is_current_task(self, screen):
        roi = screen[680:680 + 230, 520:520 + 430]

        ref = cv2.imread("../media/identifiers/card_identifier.png")
        res = cv2.matchTemplate(roi, ref, cv2.TM_CCOEFF_NORMED)

        _, m, _, _ = cv2.minMaxLoc(res)
        return m > 0.9

    def do_task(self, screen):
        pyautogui.PAUSE = 0.1

        card_x = [760, 490, 1550]
        card_y = [815, 430, 430]

        pyautogui.moveTo(card_x[0], card_y[0])
        pyautogui.click()

        time.sleep(0.35)

        pyautogui.moveTo(card_x[1], card_y[1])
        pyautogui.dragTo(card_x[2], card_y[2], 0.55)
