import cv2
import numpy as np
import pyautogui
import time

from task import Task


class FixWiring(Task):

	def __init__(self):
		self.colors = ['red', 'blue', 'yellow', 'pink']


	def is_current_task(self, screen):
		
		roi = screen[180:180 + 120, 490:490 + 200]

		for color in self.colors:
			wire_img = cv2.imread("../media/wiring_colors/{}.png".format(color))

			res = cv2.matchTemplate(roi, wire_img, cv2.TM_CCOEFF_NORMED)
			_, m, _, _ = cv2.minMaxLoc(res)
			
			if m > 0.75:
				return True

		return False


	def do_task(self, screen):

		pyautogui.PAUSE = 0.035

		for color in self.colors:
			red = cv2.imread("../media/wiring_colors/{}.png".format(color))
			red_right = cv2.imread("../media/wiring_colors/{}_right.png".format(color))

			img_cop = screen.copy()

			res = cv2.matchTemplate(img_cop, red, cv2.TM_CCOEFF_NORMED)
			min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
			top_left = max_loc

			res2 = cv2.matchTemplate(img_cop, red_right, cv2.TM_CCOEFF_NORMED)
			min_val, max_val, min_loc, max_loc2 = cv2.minMaxLoc(res2)
			top_left2 = max_loc2


			x = top_left2[0]
			y = top_left2[1]

			pyautogui.moveTo(top_left + (60, 30))
			pyautogui.mouseDown()
			pyautogui.moveTo(x + 60, y + 35)
			pyautogui.mouseUp()
