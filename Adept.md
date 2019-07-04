### ADEPT Information

- One key per book
- Book keys encrypted by a per user key (RSA with PKCS#1 v1.5 padding)
- Books are encrypted with AES CBC with random IV

## Goals

- Retrieve per-user key
- Decrypt key
- Decrypt books

# Per-user key

HKEY_CURRENT_USER\Software\Adobe\Adept\Device

the value *key* holds the *device key*, but it's encrypted to the current
windows user using crypt32.dll, and can be decrypted using CryptUnprotectData
function.

The parameters given in ineptkey by iheartcabbage to it are (indata, None,
entropy, None, None, 0, outdata) where indata is the *device key*, and entropy
is a packed struct with four values.

is the number the cpuid leaf?

cpuid0 - 'GenuineIntel' or whatever CPUID with rax set to 0x0 returns
cpuid1 - CPU id number from CPUID with rax set to 0x1, _but without the first byte_

serial - the serial number of the windows root drive
vendor - cpuid0 as bytes
signature - packed bigendian unsigned int of some bits of cpuid1, struct.pack('>I', cpuid1)[1:]
user - Windows user name (string)

these values are packed: struct.pack('>I12s3s13s', serial, vendor, signature, user)

HKEY_CURRENT_USER\Software\Adobe\Adept\Activation

contains many keys and values, the key with the default value
'privateLicenseKey' holds the *user key* that can decrypt the *device key*.

The userkey is base64 encoded, and then AES CBC encrypted

(keykey is the decrypted device key)

        userkey = userkey.decode('base64')
        userkey = AES.new(keykey, AES.MODE_CBC).decrypt(userkey)
        userkey = userkey[26:-ord(userkey[-1])]

### TODO

- write this up coherently
