#
# Windows C API calls adapted from i(heart)cabbages' grungy ineptkey.py mess:
#
# https://pastebin.com/fpwuPLCC
# http://i-u2665-cabbages.blogspot.com/2009/02/circumventing-adobe-adept-drm-for-epub.html

import ctypes
import ctypes.wintypes

MAX_PATH=256
USERNAME_MAX=32

########################################################################
# advapi32.dll
########################################################################

_advapi32=ctypes.windll.advapi32

_advapi32.GetUserNameW.argtypes = [
	ctypes.c_wchar_p,
	ctypes.POINTER(ctypes.c_uint)
]

_advapi32.GetUserNameW.restype = ctypes.c_uint

def GetUserName():
	buffer = ctypes.create_unicode_buffer(USERNAME_MAX)
	size = ctypes.c_uint(len(buffer))

	_advapi32.GetUserNameW(buffer, ctypes.byref(size))

	return buffer.value

########################################################################
# kernel32.dll
########################################################################


# Alledgely ctypes.windll.kernel32 is broken on 64-bit python
#_kernel32 = ctypes.CDLL("kernel32.dll")
_kernel32 = ctypes.windll.kernel32

_kernel32.GetSystemDirectoryW.argtypes = [
	ctypes.c_wchar_p,
	ctypes.c_uint
]

_kernel32.GetSystemDirectoryW.restype = ctypes.c_uint


def GetSystemDirectory():
	buffer = ctypes.create_unicode_buffer(MAX_PATH)

	_kernel32.GetSystemDirectoryW(buffer, len(buffer))

	return buffer.value

_kernel32.GetVolumeInformationW.argtypes = [
	ctypes.c_wchar_p,
	ctypes.c_wchar_p,
	ctypes.c_uint,
	ctypes.POINTER(ctypes.c_uint),
	ctypes.POINTER(ctypes.c_uint),
	ctypes.POINTER(ctypes.c_uint),
	ctypes.c_wchar_p,
	ctypes.c_uint
]

_kernel32.GetVolumeInformationW.restype = ctypes.c_uint

def GetVolumeSerialNumber(path=None):
	vsn = ctypes.c_uint(0)

	if not path:
		path=GetSystemDirectory().split('\\')[0] + '\\'

	_kernel32.GetVolumeInformationW(path, None, 0, ctypes.byref(vsn),
		None, None, None, 0)

	return vsn.value

MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
MEM_RELEASE = 0x8000

PAGE_RWX = 0x40

_kernel32.VirtualAlloc.argtypes = [
	ctypes.wintypes.LPVOID,
	ctypes.c_size_t,
	ctypes.wintypes.DWORD,
	ctypes.wintypes.DWORD
]

_kernel32.VirtualAlloc.restype = ctypes.wintypes.LPVOID

def VirtualAlloc(addr, size, alloctype=(MEM_RESERVE | MEM_COMMIT), protect=PAGE_RWX):
	return _kernel32.VirtualAlloc(addr, size, alloctype, protect)

_kernel32.VirtualFree.argtypes = [
	ctypes.wintypes.LPVOID,
	ctypes.c_size_t,
	ctypes.wintypes.DWORD
]

_kernel32.VirtualFree.restype = ctypes.wintypes.BOOL

def VirtualFree(addr, size=0, freetype=MEM_RELEASE):
	return _kernel32.VirtualFree(addr, size, freetype)

########################################################################
# crypt32.dll
########################################################################

_crypt32=ctypes.windll.crypt32

class DATA_BLOB(ctypes.Structure):
	_fields_ = [
		('cbData', ctypes.c_uint),
		('pbData', ctypes.c_void_p)
	]

_crypt32.CryptUnprotectData.argtypes = [
	ctypes.POINTER(DATA_BLOB),
	ctypes.c_wchar_p,
	ctypes.POINTER(DATA_BLOB),
	ctypes.c_void_p,
	ctypes.c_void_p,
	ctypes.c_uint,
	ctypes.POINTER(DATA_BLOB)
]

_crypt32.CryptUnprotectData.restype = ctypes.c_uint

def CryptUnprotectData(data, key):
	indatab = ctypes.create_string_buffer(data)
	indata = DATA_BLOB(len(data), ctypes.cast(indatab, ctypes.c_void_p))

	inkeyb = ctypes.create_string_buffer(key)
	inkey = DATA_BLOB(len(key), ctypes.cast(inkeyb, ctypes.c_void_p))

	outdata = DATA_BLOB()

	if not _crypt32.CryptUnprotectData(ctypes.byref(indata), None,
		ctypes.byref(inkey), None, None, 0, ctypes.byref(outdata)):

		raise NativeException('Failed to decrypt data using CryptUnprotectData')

	return ctypes.string_at(outdata.pbData, outdata.cbData)

class NativeException(Exception):
	pass
