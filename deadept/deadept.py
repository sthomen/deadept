import io
from zipfile import ZipFile
from shutil import copyfile
from base64 import b64decode
from zlib import decompress

from Crypto.Cipher import AES, PKCS1_v1_5

from deadept.book import EncryptionIndex, LicenseToken
from deadept.platform import PlatformSelector

class DeAdept(object):
	def __init__(self, fn, platform=None):
		selector = PlatformSelector()

		if not platform:
			platform = selector.default()
		
		self.platform = selector.load(platform)

		self.fn = fn

	def getKey(self):
		return self.platform.getKey()

	def decrypt(self, outfn=None):
		if not outfn:
			outfn = self.fn

		outbytes = io.BytesIO()
		outfile = ZipFile(outbytes, 'w')

		with ZipFile(self.fn, 'r') as infile:
			try:
				with infile.open('META-INF/encryption.xml') as data:
					index = EncryptionIndex(data.read())

				with infile.open('META-INF/rights.xml') as data:
					rights = LicenseToken(data.read())
			except KeyError:
				index = None
				rights = None

			if not (rights and index):
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

				zi.file_size = len(data)

				with outfile.open(zi, 'w') as f:
					f.write(data)

			outfile.close()
			outbytes.seek(io.SEEK_SET)

			with open(outfn, 'bw') as f:
				f.write(outbytes.read())

class DeAdeptException(Exception):
	pass
