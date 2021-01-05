
import pyautogui
import cv2
import numpy as np

import time


from task import Task


class UnlockManifolds(Task):

	def is_current_task(self, screen):

		num_img = cv2.imread("../media/unlock_manifolds_numbers/10.png")
		roi = screen[380:380 + 315, 575:575 + 770]
		res = cv2.matchTemplate(roi, num_img, cv2.TM_CCOEFF_NORMED)
		_, m, _, _ = cv2.minMaxLoc(res)

		return m > 0.8

	def do_task(self, screen):

		pyautogui.PAUSE = 0.025

		# We need to take a new screenshot here, because is_current_task will already return true when the numbers are still moving
		time.sleep(0.1)

		screen = pyautogui.screenshot()
		screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

		roi = screen[380:380 + 315, 575:575 + 770]

		side_length = 138

		for i in range(1, 11):
			num_img = cv2.imread("../media/unlock_manifolds_numbers/{}.png".format(i))
			gray_num_img = cv2.cvtColor(num_img, cv2.COLOR_BGR2GRAY)
			otsu_num_img = cv2.threshold(gray_num_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

			gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
			otsu_roi = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
			res = cv2.matchTemplate(otsu_roi, otsu_num_img, cv2.TM_CCOEFF_NORMED)
			_, m, _, loc = cv2.minMaxLoc(res)

			x = loc[0]
			y = loc[1]

			pyautogui.moveTo(x + 575 + side_length / 2, y + 380 + side_length / 2)
			pyautogui.click()
