from abc import ABC, abstractmethod


class Task(ABC):

	@abstractmethod
	def is_current_task(self, screen):
		pass

	@abstractmethod
	def do_task(self, screen):
		pass





