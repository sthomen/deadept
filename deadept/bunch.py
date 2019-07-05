class Bunch(dict):
	def __getattr__(self, key):
		if key in self:
			return self.get(key)

		try:
			return dict.__getattr__(self, key)
		except AttributeError:
			return None

	def __setattr__(self, key, value):
			self[key] = value
