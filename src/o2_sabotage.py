import numpy as np
import pyautogui
import imutils
import cv2
import time
import pytesseract


from task import Task


class O2Sabotage(Task):

	def __init__(self):
		self.button_locations = {
			1: (800, 380),
			2: (960, 380),
			3: (1110, 380),
			4: (800, 540),
			5: (960, 540),
			6: (1110, 540),
			7: (800, 710),
			8: (960, 710),
			9: (1110, 710),
			0: (960, 860)
		}

	def is_current_task(self, screen):
		roi = screen[780:780 + 200, 720:720 + 490]

		ref = cv2.imread("../media/identifiers/o2sabotage_identifier.png")
		res = cv2.matchTemplate(roi, ref, cv2.TM_CCOEFF_NORMED)

		_, m, _, _ = cv2.minMaxLoc(res)
		return m > 0.9

	def do_task(self, screen):

		x = [1220, 40]
		y = [202, 140]

		w = [250, 140]
		h = [200, 50]

		rotation_angle = 28

		image = screen[y[0]:y[0] + h[0], x[0]:x[0] + w[0]]

		rotated = imutils.rotate_bound(image, rotation_angle)
		gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
		code_area = gray[y[1]:y[1] + h[1], x[1]:x[1] + w[1]]

		kernel = np.ones((3, 3), np.uint8)
		erosion = cv2.erode(code_area, kernel, iterations=1)

		pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
		code = pytesseract.image_to_string(erosion)

		# 5 is often misclassified as 'S' or 's'
		code = code.replace('s', '5')
		code = code.replace('S', '5')

		for k in code:
			if k.isnumeric():
				i = int(k)
				pyautogui.moveTo(self.button_locations[i])
				pyautogui.click()

		enter_button = (1110, 860)
		pyautogui.moveTo(enter_button)
		pyautogui.click()

		time.sleep(3)

