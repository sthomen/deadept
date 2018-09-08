import platform

class DeAdept(object):
	def __init__(self):
		# XXX
		# Import platform-specific key extractors, this masquerades as the
		# Platform class (They all share the same base class). The alternative
		# would be to use getattr(), and I don't see the difference here.
		# I'm sure there's a proper OO way of doing this but for now this can
		# stand.

		if platform.system() == 'Windows':
			from .win import Windows as Platform
		else:
			raise DeAdeptException('Unsupported platform: {}'.format(platform.system()))

		self.platform=Platform()

	def getDeviceKey(self):
		return self.platform.getDeviceKey()

	def getKey(self):
		return self.platform.getKey()

class DeAdeptException(Exception):
	pass
