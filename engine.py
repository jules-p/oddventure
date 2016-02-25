class Engine(object):

	def __init__(self, scene_map):
		self.scene_map = scene_map

	def play(self):
		current_scene = self.scene_map.opening_scene()

		while True:
			current_scene.enter()
			next_scene_name = current_scene.action()
			current_scene = self.scene_map.next_scene(next_scene_name)