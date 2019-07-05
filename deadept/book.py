import re
import xml.etree.ElementTree as ET

from .bunch import Bunch

class EncryptionIndex(list):
	"""
	Parse an Adept encryption.xml index
	"""
	def __init__(self, data=None, filename=None):
		if not data:
			if filename:
				with open(filneame) as fp:
					data = fp.read()
			else:
				raise BookException('Missing parameters to EncryptionIndex, either data or filename must be provided')

		self.data = data
		self.load(self.data)

	def load(self, data):
		del self[:]
		root = ET.fromstring(data)

		for child in root:
			entry = EncryptionIndexEntry()

			ns = None
			match = re.match(r'{([^}]+)}.+', child.tag)

			if match:
				ns = match.group(1)

			method = child.find(f'{{{ns}}}EncryptionMethod')

			if method != None and 'Algorithm' in method.attrib:
				*_, algorithm = method.attrib.get('Algorithm').split('#')
				entry.algorithm = algorithm

			reference = child.find(f'{{{ns}}}CipherData/{{{ns}}}CipherReference')

			if reference != None and 'URI' in reference.attrib:
				entry.path = reference.attrib.get('URI')

			self.append(entry)

	def find(self, path):
		for entry in self:
			if entry.path == path:
				return entry

		return None

class EncryptionIndexEntry(Bunch):
	def __init__(self):
		self.path = None
		self.method = None

class LicenseToken(Bunch):
	def __init__(self, data):
		self.load(data)

	def load(self, data):
		self.clear()
		root = ET.fromstring(data)

		ns = None
		match = re.match(r'{([^}]+)}.+', root.tag)

		if match:
			ns = match.group(1)

		token = root.find(f'{{{ns}}}licenseToken')

		for child in token:
			self[re.sub(r'^{[^}]+}', '', child.tag)] = child.text

class BookException(Exception):
	pass
