from Crypto.PublicKey import RSA

from ..platform import Platform, PlatformException

class Keyfile(Platform):
	def getKey(self):
		try:
			with open('adept.der', 'br') as fp:
				data = fp.read()
		except (IOError, FileNotFoundError):
			raise PlatformException("Couldn't load user key from 'adept.der' in the current directory")

		return RSA.import_key(data)
