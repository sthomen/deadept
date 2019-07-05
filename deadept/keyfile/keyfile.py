from Crypto.PublicKey import RSA

from ..platform import Platform, PlatformException

class Keyfile(Platform):
	def getKey(self):
		with open('adept.der', 'br') as fp:
			data = fp.read()

		return RSA.import_key(data)
