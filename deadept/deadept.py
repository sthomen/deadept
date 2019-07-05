import platform
import io
import re
from zipfile import ZipFile
from shutil import copyfile
from base64 import b64decode
from zlib import decompress

from Crypto.Cipher import AES, PKCS1_v1_5

from deadept.book import EncryptionIndex, LicenseToken, Container

class DeAdept(object):
	def __init__(self, fn):
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

		self.fn = fn

	def getDeviceKey(self):
		return self.platform.getDeviceKey()

	def getKey(self):
		return self.platform.getKey()

	def decrypt(self, outfn=None):
		outbytes = io.BytesIO()

		if not outfn:
			outfn = self.fn

		with ZipFile(self.fn, 'r') as infile, ZipFile(outbytes, 'w') as outfile:
			index = None
			rights = None

			with infile.open('META-INF/encryption.xml') as data:
				index = EncryptionIndex(data.read())

			with infile.open('META-INF/rights.xml') as data:
				rights = LicenseToken(data.read())

			if not rights and index:
				raise DeAdeptException("Couldn't load the encryption index and license token, does this epub really use the Adept DRM?")

			rsa_cipher = PKCS1_v1_5.new(self.getKey())
			bookkey = rsa_cipher.decrypt(b64decode(rights.encryptedKey), None)

			for zi in infile.infolist():
				if zi.filename in ('META-INF/encryption.xml', 'META-INF/rights.xml'):
					continue

				with infile.open(zi.filename, 'r') as f:
					data = f.read()

				if index.find(zi.filename):
					compressed = AES.new(bookkey, AES.MODE_CBC).decrypt(data)

					# As per ineptepub.py the decoded file is apparently still compressed,
					# but has a 16 byte header of some kind. The script also seems to suggest
					# there's a suffix, but it apparently isn't necessary to remove it.
					data = decompress(compressed[16:], wbits=-15)

				elif zi.filename == 'META-INF/container.xml':
					data = bytes(Container(data).changeToFree())	# This replaces OPS/ with OEBPS/ in the container

				# Change any file with OPS in the path to OEBPS, this makes these books work on my kobo
				zi.filename = re.sub(r'^OPS/', 'OEBPS/', zi.filename)
				zi.file_size = len(data)

				with outfile.open(zi, 'w') as f:
					f.write(data)

			outbytes.seek(io.SEEK_SET)

			with open(outfn, 'bw') as f:
				f.write(outbytes.read())

class DeAdeptException(Exception):
	pass
