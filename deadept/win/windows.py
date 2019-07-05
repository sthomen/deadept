import struct
from base64 import b64decode

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util import Padding
import wmi

from .registry import Registry
from .native import GetUserName, GetVolumeSerialNumber, CryptUnprotectData

from ..platform import Platform, PlatformException

class Windows(Platform):
	REG_PATH_DEVICE='Software\Adobe\Adept\Device'
	REG_PATH_ACTIVATION='Software\Adobe\Adept\Activation'
	REG_KEY_DEVICE='key'
	REG_KEY_ACTIVATION='privateLicenseKey'
	REG_SUBKEY_ACTIVATION='value'

	def getDeviceKey(self):
		# this should be the encrypted key
		try:
			data=Registry.getValue(Windows.REG_KEY_DEVICE, Windows.REG_PATH_DEVICE)
		except:
			raise PlatformException("Couldn't load the device key from windows registry")

		client = wmi.WMI()
		processor = client.Win32_Processor()[0]

		signature = struct.pack('>I', int(processor.ProcessorId[8:16], 16))[1:]

		vendor = bytes(processor.Manufacturer, 'ascii')

		serial = GetVolumeSerialNumber()
		user = GetUserName().encode()

		key=struct.pack('>I12s3s13s', serial, vendor, signature, user)

		return CryptUnprotectData(data, key)

	def getKey(self):
		device_key = self.getDeviceKey()

		try:
			plk = Registry.recursiveFindKeyWithValue(Windows.REG_KEY_ACTIVATION, Windows.REG_PATH_ACTIVATION)
			value = Registry.getValue(Windows.REG_SUBKEY_ACTIVATION, None, plk)
		except:
			raise PlatformException("Couldn't find the activation key in the windows registry")

		key = AES.new(device_key, AES.MODE_CBC).decrypt(b64decode(value))

		# as per ineptkey.py userkey = userkey[26:-ord(userkey[-1])]
		# This should be equivalent because we're using bytes here and the individual
		# elements are already integers.
		key = key[26:-key[-1]]

		return RSA.import_key(key)
