from Crypto.Cipher import AES
from Crypto.Util import Padding
import struct

from .registry import Registry
from .native import GetUserName, GetVolumeSerialNumber, CryptUnprotectData

from ..platform import Platform

class Windows(Platform):
	REG_PATH_DEVICE='Software\Adobe\Adept\Device'
	REG_PATH_ACTIVATION='Software\Adobe\Adept\Activation'
	REG_KEY_DEVICE='key'
	REG_KEY_ACTIVATION='privateLicenseKey'

	def getDeviceKey(self):
		# this should be the encrypted key
		data=Registry.getValue(Windows.REG_KEY_DEVICE, Windows.REG_PATH_DEVICE)

		if not data:
			raise PlatformException('Device key not found')

		# TODO --- Figure out this bit here. What should cpuid0 and cpuid1 be?

		cpuid0 = b"foobar"
		cpuid1 = b"123456"

		vendor = cpuid0
		signature = struct.pack('>I', int(cpuid1[1:]))

		# TODO ---

		serial = GetVolumeSerialNumber()
		user = GetUserName().encode()

		key=struct.pack('>I12s3s13s', serial, vendor, signature, user)
		
		return CryptUnprotectData(data, key)


	def getKey(self):
		device_key = self.getDeviceKey()

		plk = Registry.recursiveFindKeyWithValue(Windows.REG_KEY_ACTIVATION, Windows.REG_PATH_ACTIVATION)

		if not plk:
			raise PlatformException('User (activation) key not found')

		key = AES.new(device_key, AES.MODE_CBC).decrypt(plk.decode('base64'))

		return key
