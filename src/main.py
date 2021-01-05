from fix_wiring import FixWiring
from o2_sabotage import O2Sabotage
from swipe_card import SwipeCard
from unlock_manifolds import UnlockManifolds
from sort_samples import SortSamples
from fix_weather_node import FixWeatherNode
from empty_garbage import EmptyGarbage
from calibrate_distributor import CalibrateDistributor

import pyautogui
import cv2
import numpy as np

import time

fix_wiring = FixWiring()
o2 = O2Sabotage()
swipe_card = SwipeCard()
unlock_manifolds = UnlockManifolds()
sort_samples = SortSamples()
fix_weather_node = FixWeatherNode()
empty_garbage = EmptyGarbage()
calibrate_distributor = CalibrateDistributor()

task_list = [fix_wiring,
             o2,
             swipe_card,
             unlock_manifolds,
             sort_samples,
             fix_weather_node,
             empty_garbage,
             calibrate_distributor]

quit = False

while not quit:
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

    for task in task_list:
        if task.is_current_task(screen):
            task.do_task(screen)
            break
