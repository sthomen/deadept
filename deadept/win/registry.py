import winreg

# The windows registry looks like this, with these names
#
# Key		<- can be a root key like HKEY_CLASSES_ROOT
#  +- Key
#  +- Key
#      +- Key
#  +- Key
#      +- Key
#          +- Value
#               +- Name, Type, Data
#               +- Name, Type, Data
#               +- Name, Type, Data
#               +- Name, Type, Data
#          +- Value
#               +- Name, Type, Data
#               +- Name, Type, Data
# etc
#

class Registry(object):
	"""
	This class attempts to hide some of the uglyness of winreg
	"""
	@staticmethod
	def getValue(name, path, root=winreg.HKEY_CURRENT_USER):
		"""
		"""
		if path:
			key=winreg.OpenKey(root, path)
		else:
			key=root

		data=winreg.QueryValueEx(key, name)

		# Tuple of data and type, we don't care about the type (I think)
		return data[0]

	@staticmethod
	def recursiveFindKeyWithValue(data, path, name='', root=winreg.HKEY_CURRENT_USER):
		"""
		This method traverses the key hierarchy starting at *root* looking for
		a key with a value with name *name* and data *data*.
		"""
		start=winreg.OpenKey(root, path)

		try:
			default=winreg.QueryValueEx(start, name)
			if default[0] == data:
				return start
		except WindowsError as e:
			if e.winerror == 2: # "File" not found, no such value
				pass


		# Look for children of this key. This could probably be rewritten as a
		# generator, but I have lost interest.
		i=0
		while True:
			try:
				subpath=winreg.EnumKey(start, i)
				result=Registry.recursiveFindKeyWithValue(data, subpath, name, start)

				if result:
					return result

				i=i+1
			except WindowsError as e:
				if e.winerror == 259:	# No more children
					return None
