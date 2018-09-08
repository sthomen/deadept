#!/usr/bin/env python3

#from deadept import DeAdept

#da=DeAdept()

#print(da.getKey())

import ctypes
import struct

from deadept.win.native import GetVolumeSerialNumber, VirtualAlloc, VirtualFree

CPUID0_INSNS = [
	0x49, 0x89, 0xd8,	# mov    %rbx,%r8
	0x49, 0x89, 0xc9,	# mov    %rcx,%r9
	0x48, 0x31, 0xc0,	# xor    %rax,%rax
	0x0f, 0xa2,			# cpuid
	0x4c, 0x89, 0xc8,	# mov    %r9,%rax
	0x89, 0x18,			# mov    %ebx,0x0(%rax)
	0x89, 0x50, 0x04,	# mov    %edx,0x4(%rax)
	0x89, 0x48, 0x08,	# mov    %ecx,0x8(%rax)
	0x4c, 0x89, 0xc3,	# mov    %r8,%rbx
	0xc3				# retq
]

CPUID1_INSNS = [
	0x53,				# push   %rbx
	0x48, 0x31, 0xc0,	# xor    %rax,%rax
	0x48, 0xff, 0xc0,	# inc    %rax
	0x0f, 0xa2,			# cpuid
	0x5b,				# pop    %rbx
	0xc3				# retq
]

class ASMFunc(object):
	def __init__(self, insns, restype, *argtypes):
		size = len(insns)
		code = (ctypes.c_ubyte * size)(*insns)
		self._addr = VirtualAlloc(None, size)
		ctypes.memmove(self._addr, code, size)
		ftype = ctypes.CFUNCTYPE(restype, *argtypes)
		self._func = ftype(self._addr)

	def __call__(self, *args):
		self._func(*args)

	def __del__(self):
		if self._addr:
			VirtualFree(self._addr)
			self._addr = None

def cpuid0():
	_cpuid0 = ASMFunc(CPUID0_INSNS, None, ctypes.c_char_p)

	buf = ctypes.create_string_buffer(12)

	_cpuid0(buf)

	return buf.raw

def cpuid1():
	_cpuid1 = ASMFunc(CPUID1_INSNS, ctypes.c_uint)
	return _cpuid1()

print("serial = {}".format(hex(GetVolumeSerialNumber())))
print("CPUID0 = {}".format(repr(cpuid0())))
print("CPUID1 = {}".format(cpuid1()))
