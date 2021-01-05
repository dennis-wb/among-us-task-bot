import pyautogui
import cv2
import numpy as np

import time

from task import Task


class FixWeatherNode(Task):

	def is_current_task(self, screen):
		roi = screen[176:176 + 105, 325:325 + 500]

		ref = cv2.imread("../media/identifiers/fix_weather_node_identifier.png")
		res = cv2.matchTemplate(roi, ref, cv2.TM_CCOEFF_NORMED)

		_, m, _, _ = cv2.minMaxLoc(res)
		
		return m > 0.9

	def do_task(self, screen):

		top_left = (493, 370)

		bottom_right = (1422, 624)
		roi = screen[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

		horizontal_wall = cv2.imread("../media/fix_weather_nodes_images/horizontal_wall.png")
		vertical_wall = cv2.imread("../media/fix_weather_nodes_images/vertical_wall.png")

		res1 = cv2.matchTemplate(roi, horizontal_wall, cv2.TM_CCOEFF_NORMED)
		res2 = cv2.matchTemplate(roi, vertical_wall, cv2.TM_CCOEFF_NORMED)

		threshold = 0.90

		horizontal_loc = np.where(res1 >= threshold)
		vertical_loc = np.where(res2 >= threshold)

		maze = np.zeros((5, 17))

		for i in range(17):
			if i % 2 == 1:
				maze[1][i] = 1
				maze[3][i] = 1

		possible_horizontal_walls_x = [0, 111, 223, 335, 446, 558, 669, 781, 893]
		possible_horizontal_walls_y = [49, 161]

		possible_vertical_walls_x = [56, 167, 279, 390, 502, 614, 725, 837]
		possible_vertical_walls_y = [0, 110, 219]

		epsilon = 10

		horizontals_found = []
		for pt in zip(*horizontal_loc[::-1]):
			found = False
			for i, x in enumerate(possible_horizontal_walls_x):
				for j, y in enumerate(possible_horizontal_walls_y):
					if abs(pt[0] - x) < epsilon and abs(pt[1] - y) < epsilon:
						maze[2*j + 1][2*i] = 1
						found = True
						break

				if found:
					break

		v = []
		for pt in zip(*vertical_loc[::-1]):
			found = False
			for i, x in enumerate(possible_vertical_walls_x):
				for j, y in enumerate(possible_vertical_walls_y):
					if abs(pt[0] - x) < epsilon and abs(pt[1] - y) < epsilon:
						maze[2*j][2*i + 1] = 1
						if (j, i) not in v:
							v.append((j, i))
						found = True
						break

				if found:
					break


		path = self.bfs(maze)

		pyautogui.PAUSE = 0.04

		# move to (0, 0) first

		pyautogui.moveTo(515, 328)
		pyautogui.mouseDown()
		pyautogui.move(0, 55)

		lastPoint = (0, 0)
		for point in path[1:]:
			x_diff = point[0] - lastPoint[0]
			y_diff = point[1] - lastPoint[1]
			pyautogui.move(55 * x_diff, 55 * y_diff)

			lastPoint = point

		# move to end node
		pyautogui.move(0, 55)
		pyautogui.mouseUp()

		time.sleep(1)


	def neighbors(self, node, maze):

		x = node[0]
		y = node[1]

		ret = [(x+1, y), (x, y+1), (x, y-1), (x-1, y)]

		w = len(maze[0])
		h = len(maze)

		toRemove = []
		for i in ret:
			if i[0] < 0 or i[1] < 0:
				toRemove.append(i)
				continue
			if i[0] >= w or i[1] >= h:
				toRemove.append(i)
				continue

		
		ret_final = []
		for i in ret:
			if i not in toRemove:
				ret_final.append(i)
		return ret_final


	def bfs(self, maze):

		start = (0, 0)
		end = (16, 4)

		visited = []
		toVisit = []
		endFound = False

		cameFrom = {}
	
		while not endFound:

			if toVisit:
				cur = toVisit.pop(0)
			else:
				cur = start

			if cur == end:
				endFound = True


				nodeBefore = None
				j = 0

				ret = []
				while nodeBefore != (start[0], start[1]):
					nodeBefore = cameFrom[cur]
					cur = nodeBefore
					ret.append(nodeBefore)
					j += 1

				ret.reverse()
				ret.append(end)
				return ret



			n = self.neighbors(cur, maze)

			visited.append(cur)

			for q in n:
				if q not in visited:
					if maze[q[1]][q[0]] == 0:
						if q not in toVisit:
							toVisit.append((q[0], q[1]))
							cameFrom[q] = cur

