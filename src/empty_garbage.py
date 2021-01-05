import cv2
import pyautogui
import time

from task import Task


class EmptyGarbage(Task):

    def is_current_task(self, screen):
        roi = screen[140:140 + 200, 1200:1200 + 170]

        ref = cv2.imread("../media/identifiers/empty_garbage_identifier.png")
        res = cv2.matchTemplate(roi, ref, cv2.TM_CCOEFF_NORMED)

        _, m, _, _ = cv2.minMaxLoc(res)
        return m > 0.9

    def do_task(self, screen):
        pyautogui.moveTo(1280, 415)
        pyautogui.mouseDown()
        pyautogui.move(0, 400)
        time.sleep(2)
        pyautogui.mouseUp()
        time.sleep(1)
