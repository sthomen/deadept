class Platform(object):
	def getKey(self):
		return None

class PlatformSelector(object):
	DEFAULT = 'windows'

	PLATFORMS = {
		'windows': 'deadept.win.windows.Windows'
	}

	def default(self):
		return self.DEFAULT

	def platforms(self):
		return list(self.PLATFORMS.keys())

	def load(self, platform):
		if not platform in self.PLATFORMS:
			raise PlatformSelectorException(f'Unsupported platform {platform}')

		module, name = self.PLATFORMS[platform].rsplit('.', 1)

		platform = __import__(module, fromlist=[ name ])

		return getattr(platform, name)()

class PlatformException(Exception):
	pass

class PlatformSelectorException(Exception):
	pass
