import cv2
import pyautogui

from task import Task


class SortSamples(Task):
    samples = ['gem1', 'gem2', 'animal_fossil1', 'animal_fossil2', 'plant_fossil1', 'plant_fossil2']

    def is_current_task(self, screen):
        x, y, w, h = 370, 730, 1130, 340
        roi = screen[y:y + h, x:x + w]

        ref = cv2.imread("../media/sort_samples_images/gem1.png")
        res = cv2.matchTemplate(roi, ref, cv2.TM_CCOEFF_NORMED)

        _, m, _, _ = cv2.minMaxLoc(res)

        return m > 0.9

    def do_task(self, screen):
        x, y, w, h = 370, 730, 1130, 340
        roi = screen[y:y + h, x:x + w]

        gem_location = (625, 570)
        plant_location = (1270, 610)
        animal_location = (970, 210)

        for sample in self.samples:

            img = cv2.imread("../media/sort_samples_images/{}.png".format(sample))
            res = cv2.matchTemplate(roi, img, cv2.TM_CCOEFF_NORMED)

            _, _, _, max_loc = cv2.minMaxLoc(res)
            top_left = max_loc
            x1 = top_left[0] + x
            y1 = top_left[1] + y
            pyautogui.moveTo(x1 + 75, y1 + 50)

            pyautogui.mouseDown()
            if 'gem' in sample:
                pyautogui.moveTo(gem_location)
            elif 'animal' in sample:
                pyautogui.moveTo(animal_location)
            elif 'plant' in sample:
                pyautogui.moveTo(plant_location)
            pyautogui.mouseUp()
